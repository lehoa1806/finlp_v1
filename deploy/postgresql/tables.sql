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
GRANT SELECT, INSERT, UPDATE, DELETE ON "malaysia_announcements" TO xxxxx_user;

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
GRANT SELECT, INSERT, UPDATE, DELETE ON "malaysia_articles" TO xxxxx_user;

-- malaysia_companies
CREATE TABLE IF NOT EXISTS "malaysia_companies" (
  "stock_id" TEXT UNIQUE NOT NULL,
  "short_name" TEXT NOT NULL,
  "name" TEXT NOT NULL,
  "industry" TEXT NOT NULL,
  "sector" TEXT NOT NULL,
  CONSTRAINT "malaysia_companies_stock" PRIMARY KEY ("stock_id")
);
GRANT SELECT, INSERT, UPDATE, DELETE ON "malaysia_companies" TO xxxxx_user;

-- malaysia_categories
CREATE TABLE IF NOT EXISTS "malaysia_categories" (
  "category" TEXT NOT NULL,
  "source" TEXT NOT NULL DEFAULT 'finlp',
  "subscription" INT,
  CONSTRAINT "malaysia_categories_category_source" PRIMARY KEY ("category", "source")
);
GRANT SELECT, INSERT, UPDATE, DELETE ON "malaysia_categories" TO xxxxx_user;

-- malaysia_search_keys
CREATE TABLE IF NOT EXISTS "malaysia_search_keys" (
  "search_key" TEXT UNIQUE NOT NULL,
  "subscription" INT,
  CONSTRAINT "malaysia_search_keys_search_key" PRIMARY KEY ("search_key")
);
GRANT SELECT, INSERT, UPDATE, DELETE ON "malaysia_search_keys" TO xxxxx_user;

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
GRANT SELECT, INSERT, UPDATE, DELETE ON "malaysia_news2email_all" TO xxxxx_user;

-- vietnam_announcements
CREATE TABLE IF NOT EXISTS "vietnam_announcements" (
  "modified" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  "datetime" TIMESTAMP WITH TIME ZONE,
  "company" TEXT,
  "title" TEXT NOT NULL,
  "source" TEXT,
  "url" TEXT UNIQUE NOT NULL,
  "description" TEXT,
  CONSTRAINT "vietnam_announcements_datetime_title" PRIMARY KEY ("datetime", "title")
);
GRANT SELECT, INSERT, UPDATE, DELETE ON "vietnam_announcements" TO xxxxx_user;

-- vietnam_articles
CREATE TABLE IF NOT EXISTS "vietnam_articles" (
  "modified" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  "datetime" TIMESTAMP WITH TIME ZONE,
  "category" TEXT,
  "title" TEXT NOT NULL,
  "source" TEXT,
  "url" TEXT UNIQUE NOT NULL,
  "content" TEXT,
  CONSTRAINT "vietnam_articles_datetime_title" PRIMARY KEY ("datetime", "title")
);
GRANT SELECT, INSERT, UPDATE, DELETE ON "vietnam_articles" TO xxxxx_user;

-- vietnam_warrants
CREATE TABLE IF NOT EXISTS "vietnam_warrants" (
  "modified" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  "datetime" TIMESTAMP WITH TIME ZONE,
  "warrant" TEXT NOT NULL,
  "provider" TEXT,
  "expiredDate" TIMESTAMP WITH TIME ZONE,
  "exercisePrice" INT,
  "referencePrice" INT,
  "volume" INT,
  "price" INT,
  "sharePrice" INT,
  "exerciseRatio" TEXT,
  "foreignBuy" INT,
  CONSTRAINT "vietnam_warrants_datetime_warrant" PRIMARY KEY ("datetime", "warrant")
);
GRANT SELECT, INSERT, UPDATE, DELETE ON "vietnam_warrants" TO xxxxx_user;

-- vietnam_estimated_prices
CREATE TABLE IF NOT EXISTS "vietnam_estimated_prices" (
  "modified" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  "name" TEXT NOT NULL PRIMARY KEY,
  "price" INT
 );
GRANT SELECT, INSERT, UPDATE, DELETE ON "vietnam_estimated_prices" TO xxxxx_user;

-- users_watchlists
CREATE TABLE IF NOT EXISTS "users_watchlists" (
  "modified" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  "user" TEXT NOT NULL,
  "watchlist" TEXT NOT NULL,
  "warrants" JSON,
  CONSTRAINT "users_watchlists_user_watchlist" PRIMARY KEY ("user", "watchlist")
);
GRANT SELECT, INSERT, UPDATE, DELETE ON "users_watchlists" TO xxxxx_user;

-- users_portfolio
CREATE TABLE IF NOT EXISTS "users_portfolio" (
  "modified" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  "datetime" TIMESTAMP WITH TIME ZONE,
  "user" TEXT NOT NULL,
  "warrant" TEXT NOT NULL,
  "quantity" INT NOT NULL,
  "acquisitionPrice" INT NOT NULL,
  CONSTRAINT "users_portfolio_user_warrant" PRIMARY KEY ("user", "warrant")
);
GRANT SELECT, INSERT, UPDATE, DELETE ON "users_portfolio" TO xxxxx_user;

-- users_history
CREATE TABLE IF NOT EXISTS "users_history" (
  "modified" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  "datetime" TIMESTAMP WITH TIME ZONE,
  "user" TEXT NOT NULL,
  "recordId" TEXT NOT NULL,
  "warrant" TEXT NOT NULL,
  "action" TEXT NOT NULL,
  "quantity" INT NOT NULL,
  "price" INT NOT NULL,
  "realizedLossProfit" TEXT,
  CONSTRAINT "users_history_user_recordId" PRIMARY KEY ("user", "recordId")
);
GRANT SELECT, INSERT, UPDATE, DELETE ON "users_history" TO xxxxx_user;

-- vietnam_companies
CREATE TABLE IF NOT EXISTS "vietnam_companies" (
  "stock_id" TEXT UNIQUE NOT NULL,
  "short_name" TEXT NOT NULL,
  "name" TEXT NOT NULL,
  "industry" TEXT NOT NULL,
  "sector" TEXT NOT NULL,
  CONSTRAINT "vietnam_companies_stock" PRIMARY KEY ("stock_id")
);
GRANT SELECT, INSERT, UPDATE, DELETE ON "vietnam_companies" TO xxxxx_user;

-- vietnam_categories
CREATE TABLE IF NOT EXISTS "vietnam_categories" (
  "category" TEXT NOT NULL,
  "source" TEXT NOT NULL DEFAULT 'finlp',
  "subscription" INT,
  CONSTRAINT "vietnam_categories_category_source" PRIMARY KEY ("category", "source")
);
GRANT SELECT, INSERT, UPDATE, DELETE ON "vietnam_categories" TO xxxxx_user;

-- vietnam_search_keys
CREATE TABLE IF NOT EXISTS "vietnam_search_keys" (
  "search_key" TEXT UNIQUE NOT NULL,
  "subscription" INT,
  CONSTRAINT "vietnam_search_keys_search_key" PRIMARY KEY ("search_key")
);
GRANT SELECT, INSERT, UPDATE, DELETE ON "vietnam_search_keys" TO xxxxx_user;

-- temp tables
CREATE TABLE IF NOT EXISTS "vietnam_news2email_all" (
  "news_id" SERIAL NOT NULL,
  "modified" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  "datetime" TIMESTAMP WITH TIME ZONE,
  "category" TEXT,
  "title" TEXT NOT NULL,
  "source" TEXT,
  "url" TEXT UNIQUE NOT NULL,
  "content" TEXT,
  CONSTRAINT vietnam_news2email_news_id PRIMARY KEY (news_id)
);
GRANT SELECT, INSERT, UPDATE, DELETE ON "vietnam_news2email_all" TO xxxxx_user;
