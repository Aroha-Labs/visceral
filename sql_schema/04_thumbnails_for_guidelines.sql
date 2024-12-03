CREATE TABLE IF NOT EXISTS "public"."thumbnails_for_guidelines" (
    "id" TEXT PRIMARY KEY,
    "genre" TEXT NOT NULL,
    "encoded_image" BYTEA NOT NULL
);
