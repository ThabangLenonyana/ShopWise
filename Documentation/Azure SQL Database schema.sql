CREATE TABLE [retailers] (
  [id] integer PRIMARY KEY,
  [name] nvarchar(255),
  [created_at] DATETIME2
)
GO

CREATE TABLE [categories] (
  [id] integer PRIMARY KEY,
  [name] nvarchar(255),
  [created_at] DATETIME2
)
GO

CREATE TABLE [products] (
  [id] integer PRIMARY KEY,
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
  [id] integer PRIMARY KEY,
  [product_id] integer,
  [price] float,
  [created_at] DATETIME2
)
GO

CREATE TABLE [users] (
  [id] integer PRIMARY KEY,
  [username] nvarchar(255) UNIQUE,
  [email] nvarchar(255) UNIQUE,
  [password_hash] nvarchar(255),
  [first_name] nvarchar(255),
  [last_name] nvarchar(255),
  [created_at] DATETIME2,
)
GO

CREATE TABLE [user_favorites] (
  [id] integer PRIMARY KEY,
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


