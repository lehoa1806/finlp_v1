-- malaysia_articles
CREATE TABLE IF NOT EXISTS "malaysia_articles" (
  "modified" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  "datetime" TIMESTAMP,
  "category" TEXT,
  "title" TEXT NOT NULL,
  "source" TEXT,
  "url" TEXT UNIQUE NOT NULL,
  "content" TEXT,
  CONSTRAINT "datetime_title" PRIMARY KEY ("datetime", "title")
);

-- malaysia_companies
CREATE TABLE IF NOT EXISTS "malaysia_companies" (
  "stock_id" TEXT UNIQUE NOT NULL,
  "short_name" TEXT NOT NULL,
  "name" TEXT NOT NULL,
  "industry" TEXT NOT NULL,
  "sector" TEXT NOT NULL,
  CONSTRAINT "stock" PRIMARY KEY ("stock_id")
);

-- malaysia_categories
CREATE TABLE IF NOT EXISTS "malaysia_categories" (
  "category" TEXT NOT NULL,
  "source" TEXT NOT NULL DEFAULT 'finlp',
  "subscription" INT,
  CONSTRAINT "category_source" PRIMARY KEY ("category", "source")
);

-- malaysia_search_keys
CREATE TABLE IF NOT EXISTS "malaysia_search_keys" (
  "search_key" TEXT UNIQUE NOT NULL,
  "subscription" INT,
  CONSTRAINT "search_key" PRIMARY KEY ("search_key")
);
