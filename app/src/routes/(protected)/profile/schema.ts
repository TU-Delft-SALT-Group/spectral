import { z } from 'zod';

export const formSchema = z.object({
  key: z.string(),
});

export type FormSchema = typeof formSchema;
