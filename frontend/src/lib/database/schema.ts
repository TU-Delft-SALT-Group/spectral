import { boolean, customType, pgTable, text, timestamp } from 'drizzle-orm/pg-core';
import { sql } from 'drizzle-orm';

export const userTable = pgTable('user', {
	id: text('id').primaryKey(),
	email: text('email').unique().notNull(),
	username: text('username').notNull(),
	hashedPassword: text('hashed_password').notNull(),
	creationTime: timestamp('creation_time').default(sql`CURRENT_TIMESTAMP`),
});

export const sessionTable = pgTable('session', {
	id: text('id').primaryKey(),
	userId: text('user_id')
		.notNull()
		.references(() => userTable.id),
	expiresAt: timestamp('expires_at', {
		withTimezone: true,
		mode: 'date',
	}).notNull(),
});

const byteArray = customType<{ data: Uint8Array }>({
	dataType() {
		return 'bytea';
	},
});

export const filesTable = pgTable('files', {
	id: text('id').primaryKey(),
	name: text('id'),
	data: byteArray('data'),
	creationTime: timestamp('creation_time').default(sql`CURRENT_TIMESTAMP`),
	modifiedTime: timestamp('modified_time').default(sql`CURRENT_TIMESTAMP`),
	uploader: text('id').notNull().references(() => userTable.id),
	ephemeral: boolean('ephemeral'),
});
