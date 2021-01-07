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

-- malaysia_companies
CREATE TABLE IF NOT EXISTS "malaysia_companies" (
  "stock_id" TEXT UNIQUE NOT NULL,
  "short_name" TEXT NOT NULL,
  "name" TEXT NOT NULL,
  "industry" TEXT NOT NULL,
  "sector" TEXT NOT NULL,
  CONSTRAINT "malaysia_companies_stock" PRIMARY KEY ("stock_id")
);

-- malaysia_categories
CREATE TABLE IF NOT EXISTS "malaysia_categories" (
  "category" TEXT NOT NULL,
  "source" TEXT NOT NULL DEFAULT 'finlp',
  "subscription" INT,
  CONSTRAINT "malaysia_categories_category_source" PRIMARY KEY ("category", "source")
);

-- malaysia_search_keys
CREATE TABLE IF NOT EXISTS "malaysia_search_keys" (
  "search_key" TEXT UNIQUE NOT NULL,
  "subscription" INT,
  CONSTRAINT "malaysia_search_keys_search_key" PRIMARY KEY ("search_key")
);
