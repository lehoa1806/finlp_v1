from typing import Any, Dict, Iterator

from common.rule import Rule
from news.utils.filter import Filter
from workflow.stage import Stage

QUERY = '''
SELECT
  announcement_id,
  announcement_detail->'time' AS time,
  announcement_source AS source,
  announcement_company AS company,
  announcement_title AS title,
  announcement_detail->'description' AS description,
  announcement_url AS url
FROM
  announcement_to_slack_all
ORDER BY
  announcement_date;
'''


class AnnouncementQueryingStage(Stage):
    def __init__(
        self,
    ) -> None:
        super().__init__('Announcement2Slack Querying')
        ft = Filter()
        hot_keys = ft.lower_all(
            [' {} '.format(k)
             for k, v in ft.get_search_keys().items() if v == 1]
        )
        self.rule = Rule({
            'contains_any': [{'title': hot_keys}, {'description': hot_keys}],
        })
        self.database = ft.database

    def process(self, item: Dict) -> Iterator[Dict[str, Any]]:
        keys = (
            'announcement_id',
            'Time',
            'Source',
            'Company',
            'Title',
            'Description',
            'Url',
        )
        for data in self.database.query(query=QUERY, keys=keys):
            if self.rule({
                'title': data.get('Title').lower(),
                'description': data.get('Description').lower()
            }):
                channel = 'hotnews'
            else:
                channel = 'announcements'
            yield {
                'announcement_id': data.get('announcement_id'),
                'Channel': channel,
                'Time': data.get('Time'),
                'Source': data.get('Source'),
                'Company': data.get('Company'),
                'Title': data.get('Title'),
                'Description': data.get('Description'),
                'Url': data.get('Url'),
            }
