import {
	boolean,
	customType,
	pgTable,
	text,
	timestamp,
	doublePrecision
} from 'drizzle-orm/pg-core';
import { sql } from 'drizzle-orm';

export const userTable = pgTable('user', {
	id: text('id').primaryKey(),
	email: text('email').unique().notNull(),
	username: text('username').notNull(),
	hashedPassword: text('hashed_password').notNull(),
	creationTime: timestamp('creation_time').default(sql`CURRENT_TIMESTAMP`)
});

export const userSessionTable = pgTable('user_session', {
	id: text('id').primaryKey(),
	userId: text('user_id')
		.notNull()
		.references(() => userTable.id),
	expiresAt: timestamp('expires_at', {
		withTimezone: true,
		mode: 'date'
	}).notNull()
});

export const byteArray = customType<{ data: Buffer }>({
	dataType() {
		return 'bytea';
	},
	fromDriver(value) {
		if (typeof value === 'object' && value instanceof Uint8Array) {
			return Buffer.from(value);
		}

		throw new Error('Expected Uint8Array');
	},
	toDriver(buffer) {
		return sql`decode(${buffer.toString('base64')}, 'base64')`;
	}
});

export const filesTable = pgTable('files', {
	id: text('id').primaryKey(),
	name: text('name').notNull(),
	data: byteArray('data').notNull(),
	creationTime: timestamp('creation_time')
		.default(sql`CURRENT_TIMESTAMP`)
		.notNull(),
	modifiedTime: timestamp('modified_time')
		.default(sql`CURRENT_TIMESTAMP`)
		.notNull(),
	uploader: text('uploader').references(() => userTable.id),
	session: text('session')
		.references(() => sessionTable.id)
		.notNull(),
	ephemeral: boolean('ephemeral').notNull().default(false)
});

export const sessionTable = pgTable('session', {
	id: text('id').primaryKey(),
	name: text('name').notNull(),
	owner: text('owner')
		.notNull()
		.references(() => userTable.id),
	creationTime: timestamp('creation_time')
		.default(sql`CURRENT_TIMESTAMP`)
		.notNull(),
	modifiedTime: timestamp('modified_time')
		.default(sql`CURRENT_TIMESTAMP`)
		.notNull()
});

export const fileTranscriptionTable = pgTable('file_transcription', {
	id: text('id').primaryKey(),
	file: text('file')
		.notNull()
		.references(() => filesTable.id)
});

export const transcriptionTable = pgTable('transcription', {
	id: text('id').primaryKey(),
	fileTranscription: text('file_transcription')
		.notNull()
		.references(() => fileTranscriptionTable.id),
	start: doublePrecision('start').notNull(),
	end: doublePrecision('end').notNull(),
	value: text('value')
});
