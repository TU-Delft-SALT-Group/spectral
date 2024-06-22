import { z } from 'zod';

export const formSchema = z.object({
	username: z.string().min(2).max(50),
	email: z.string().email(),
	password: z.string().min(8).max(50),
	privacyAck: z.boolean()
});

export type FormSchema = typeof formSchema;
