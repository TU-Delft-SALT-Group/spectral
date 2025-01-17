import { boolean, customType, pgTable, text, timestamp, jsonb, json } from 'drizzle-orm/pg-core';
import { relations, sql } from 'drizzle-orm';

export const userTable = pgTable('user', {
	id: text('id').primaryKey(),
	email: text('email').unique().notNull(),
	username: text('username').unique().notNull(),
	hashedPassword: text('hashed_password').notNull(),
	creationTime: timestamp('creation_time').default(sql`CURRENT_TIMESTAMP`)
});

export const userRelations = relations(userTable, ({ many }) => ({
	files: many(fileTable)
}));

export const userSessionTable = pgTable('user_session', {
	id: text('id').primaryKey(),
	userId: text('user_id')
		.notNull()
		.references(() => userTable.id, { onDelete: 'cascade' }),
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
		} else if (typeof value === 'string') {
			const cleanedValue = value.replace(/\\x/g, '');
			const buffer = Buffer.from(cleanedValue, 'hex');
			return buffer;
		}

		throw new Error('Expected Uint8Array');
	},
	toDriver(buffer) {
		return sql`decode(${buffer.toString('base64')}, 'base64')`;
	}
});

export const fileTable = pgTable('files', {
	id: text('id').primaryKey(),
	name: text('name').notNull(),
	data: byteArray('data').notNull(),
	creationTime: timestamp('creation_time')
		.default(sql`CURRENT_TIMESTAMP`)
		.notNull(),
	modifiedTime: timestamp('modified_time')
		.default(sql`CURRENT_TIMESTAMP`)
		.notNull(),
	uploader: text('uploader')
		.references(() => userTable.id, { onDelete: 'cascade' })
		.notNull(),
	session: text('session')
		.references(() => sessionTable.id, { onDelete: 'cascade' })
		.notNull(),
	ephemeral: boolean('ephemeral').notNull().default(false),
	groundTruth: text('ground_truth').notNull().default(''),
	note: text('note').notNull().default(''),
	state: jsonb('state')
		.notNull()
		.default(sql`'{}'`)
});

export const fileRelations = relations(fileTable, ({ one }) => ({
	session: one(sessionTable, {
		fields: [fileTable.session],
		references: [sessionTable.id]
	}),

	uploader: one(userTable, {
		fields: [fileTable.uploader],
		references: [userTable.id]
	})
}));

export const sessionTable = pgTable('session', {
	id: text('id').primaryKey(),
	name: text('name').notNull(),
	owner: text('owner')
		.notNull()
		.references(() => userTable.id, { onDelete: 'cascade' }),
	creationTime: timestamp('creation_time')
		.default(sql`CURRENT_TIMESTAMP`)
		.notNull(),
	modifiedTime: timestamp('modified_time')
		.default(sql`CURRENT_TIMESTAMP`)
		.notNull(),
	state: json('state').notNull().default({})
});

export const sessionRelations = relations(sessionTable, ({ many }) => ({
	files: many(fileTable)
}));
