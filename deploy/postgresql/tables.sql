-- malaysia_announcements
CREATE TABLE IF NOT EXISTS "malaysia_announcements" (
  "modified" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  "datetime" TIMESTAMP WITH TIME ZONE,
  "company" TEXT,
  "title" TEXT NOT NULL,
  "source" TEXT,
  "url" TEXT UNIQUE NOT NULL,
  "description" TEXT,
  CONSTRAINT "malaysia_announcements_datetime_title" PRIMARY KEY ("datetime", "title")
);
GRANT USAGE, SELECT, INSERT, DELETE ON "malaysia_announcements" TO xxxxx_user;

-- malaysia_articles
CREATE TABLE IF NOT EXISTS "malaysia_articles" (
  "modified" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  "datetime" TIMESTAMP WITH TIME ZONE,
  "category" TEXT,
  "title" TEXT NOT NULL,
  "source" TEXT,
  "url" TEXT UNIQUE NOT NULL,
  "content" TEXT,
  CONSTRAINT "malaysia_articles_datetime_title" PRIMARY KEY ("datetime", "title")
);
GRANT USAGE, SELECT, INSERT, DELETE ON "malaysia_articles" TO xxxxx_user;

-- malaysia_companies
CREATE TABLE IF NOT EXISTS "malaysia_companies" (
  "stock_id" TEXT UNIQUE NOT NULL,
  "short_name" TEXT NOT NULL,
  "name" TEXT NOT NULL,
  "industry" TEXT NOT NULL,
  "sector" TEXT NOT NULL,
  CONSTRAINT "malaysia_companies_stock" PRIMARY KEY ("stock_id")
);
GRANT USAGE, SELECT, INSERT, DELETE ON "malaysia_companies" TO xxxxx_user;

-- malaysia_categories
CREATE TABLE IF NOT EXISTS "malaysia_categories" (
  "category" TEXT NOT NULL,
  "source" TEXT NOT NULL DEFAULT 'finlp',
  "subscription" INT,
  CONSTRAINT "malaysia_categories_category_source" PRIMARY KEY ("category", "source")
);
GRANT USAGE, SELECT, INSERT, DELETE ON "malaysia_categories" TO xxxxx_user;

-- malaysia_search_keys
CREATE TABLE IF NOT EXISTS "malaysia_search_keys" (
  "search_key" TEXT UNIQUE NOT NULL,
  "subscription" INT,
  CONSTRAINT "malaysia_search_keys_search_key" PRIMARY KEY ("search_key")
);
GRANT USAGE, SELECT, INSERT, DELETE ON "malaysia_search_keys" TO xxxxx_user;

-- temp tables
CREATE TABLE IF NOT EXISTS "malaysia_news2email_all" (
  "news_id" SERIAL NOT NULL,
  "modified" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  "datetime" TIMESTAMP WITH TIME ZONE,
  "category" TEXT,
  "title" TEXT NOT NULL,
  "source" TEXT,
  "url" TEXT UNIQUE NOT NULL,
  "content" TEXT,
  CONSTRAINT malaysia_news2email_news_id PRIMARY KEY (news_id)
);
GRANT USAGE, SELECT, INSERT, DELETE ON "malaysia_news2email_all" TO xxxxx_user;
