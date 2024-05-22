import { modes } from '.';
import { z } from 'zod';

/**
 * The name of a mode
 */
export type Name = keyof typeof modes;

export type ComputedData<M extends Name> = z.infer<(typeof modes)[M]['computedFileData']>;
export type ModeState<M extends Name> = z.infer<(typeof modes)[M]['modeState']>;
export type FileState<M extends Name> = z.infer<(typeof modes)[M]['fileState']>;
