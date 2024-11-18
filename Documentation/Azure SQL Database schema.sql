CREATE TABLE [retailers] (
  --IDs should auto increment
  
  [id] integer PRIMARY KEY IDENTITY(1,1),
  [name] nvarchar(255),
  [created_at] DATETIME2
)
GO

CREATE TABLE [categories] (
  [id] integer PRIMARY KEY IDENTITY(1,1),
  [name] nvarchar(255),
  [created_at] DATETIME2
)
GO

CREATE TABLE [products] (
  [id] integer PRIMARY KEY IDENTITY(1,1),
  [name] nvarchar(255),
  [image_url] nvarchar(255),
  [product_url] nvarchar(255),
  [description] text,
  [category_id] integer,
  [retailer_id] integer,
  [created_at] DATETIME2
)
GO

CREATE TABLE [prices] (
  [id] integer PRIMARY KEY IDENTITY(1,1),
  [product_id] integer,
  [price] float,
  [created_at] DATETIME2
)
GO

CREATE TABLE [Users] (
  [id] integer PRIMARY KEY IDENTITY(1,1),
  [username] nvarchar(255) UNIQUE,
  [email] nvarchar(255) UNIQUE,
  [password_hash] nvarchar(255),
  [first_name] nvarchar(255),
  [last_name] nvarchar(255),
  [created_at] DATETIME2,
)
GO

CREATE TABLE [User_favorites] (
  [id] integer PRIMARY KEY IDENTITY(1,1),
  [user_id] integer,
  [product_id] integer,
  [created_at] DATETIME2
)
GO

ALTER TABLE [user_favorites] ADD FOREIGN KEY ([user_id]) REFERENCES [users] ([id])
GO

ALTER TABLE [user_favorites] ADD FOREIGN KEY ([product_id]) REFERENCES [products] ([id])
GO

ALTER TABLE [products] ADD FOREIGN KEY ([retailer_id]) REFERENCES [retailers] ([id])
GO

ALTER TABLE [products] ADD FOREIGN KEY ([category_id]) REFERENCES [categories] ([id])
GO

ALTER TABLE [prices] ADD FOREIGN KEY ([product_id]) REFERENCES [products] ([id])
GO

ALTER TABLE [retailers]
DROP COLUMN [id];
ALTER TABLE [retailers]
ADD [id] integer PRIMARY KEY IDENTITY(1,1);

-- Ensure the 'id' column in 'categories' table is set to auto increment
ALTER TABLE [categories]
DROP COLUMN [id];
ALTER TABLE [categories]
ADD [id] integer PRIMARY KEY IDENTITY(1,1);

-- Ensure the 'id' column in 'products' table is set to auto increment
ALTER TABLE [products]
DROP COLUMN [id];
ALTER TABLE [products]
ADD [id] integer PRIMARY KEY IDENTITY(1,1);

-- Ensure the 'id' column in 'prices' table is set to auto increment
ALTER TABLE [prices]
DROP COLUMN [id];
ALTER TABLE [prices]
ADD [id] integer PRIMARY KEY IDENTITY(1,1);

-- Ensure the 'id' column in 'users' table is set to auto increment
ALTER TABLE [users]
DROP COLUMN [id];
ALTER TABLE [users]
ADD [id] integer PRIMARY KEY IDENTITY(1,1);

-- Ensure the 'id' column in 'user_favorites' table is set to auto increment
ALTER TABLE [user_favorites]
DROP COLUMN [id];
ALTER TABLE [user_favorites]
ADD [id] integer PRIMARY KEY IDENTITY(1,1);

--Drop the tables 
DROP TABLE [retailers]
DROP TABLE [categories]
DROP TABLE [products]
DROP TABLE [prices]
DROP TABLE [users]
DROP TABLE [user_favorites]
