import { generateIdFromEntropySize } from 'lucia';
import { hash, verify } from '@node-rs/argon2';
import { db } from '$lib/database';
import { userTable } from '$lib/database/schema';
import { eq } from 'drizzle-orm';

export async function createUser({
	id,
	username,
	password,
	email
}: {
	id?: string;
	username: string;
	password: string;
	email: string;
}): Promise<
	| {
			success: false;
			reason: 'email-in-use' | 'username-in-use';
	  }
	| {
			success: true;
			userId: string;
	  }
> {
	const userId = id ?? generateIdFromEntropySize(10);
	const hashedPassword = await hash(password, {
		// recommended minimum parameters
		memoryCost: 19456,
		timeCost: 2,
		outputLen: 32,
		parallelism: 1
	});

	const [existingEmailUser, existingNameUser] = await Promise.all([
		db.query.userTable.findFirst({
			where: eq(userTable.email, email),
			columns: { email: false }
		}),
		db.query.userTable.findFirst({
			where: eq(userTable.username, username),
			columns: { username: false }
		})
	]);

	if (existingEmailUser !== undefined) {
		return {
			success: false,
			reason: 'email-in-use'
		};
	}

	if (existingNameUser !== undefined) {
		return {
			success: false,
			reason: 'username-in-use'
		};
	}

	await db.insert(userTable).values({
		id: userId,
		username,
		hashedPassword,
		email
	});

	return {
		success: true,
		userId
	};
}

export async function verifyUser({
	username,
	password
}: {
	username: string;
	password: string;
}): Promise<typeof userTable.$inferSelect | null> {
	const existingUser = await db.query.userTable.findFirst({
		where: eq(userTable.username, username)
	});

	if (!existingUser) {
		return null;
	}

	const isPasswordValid = await verify(existingUser?.hashedPassword, password, {
		memoryCost: 19456,
		timeCost: 2,
		outputLen: 32,
		parallelism: 1
	});

	if (!isPasswordValid) {
		return null;
	}

	return existingUser;
}
