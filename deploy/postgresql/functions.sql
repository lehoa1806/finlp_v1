-- trigger to insert new articles to malaysia_news2email_all
CREATE OR REPLACE FUNCTION "public"."insert_malaysia_news2email_all" ( ) RETURNS "pg_catalog"."trigger" AS $BODY$
  BEGIN
    INSERT INTO "malaysia_news2email_all" ( "modified", "datetime", "category", "title", "source", "url" )
  VALUES
	( NEW."modified", NEW."datetime", NEW."category", NEW."title", NEW."source", NEW."url" );
  RETURN NEW;
END;
$BODY$ LANGUAGE plpgsql VOLATILE COST 100;

CREATE TRIGGER "insert_malaysia_news2email_all" AFTER INSERT ON "public"."malaysia_articles" FOR EACH ROW
EXECUTE PROCEDURE "public"."insert_malaysia_news2email_all" ( );

GRANT USAGE, SELECT ON SEQUENCE "malaysia_news2email_all_news_id_seq" TO xxxxx_user;
