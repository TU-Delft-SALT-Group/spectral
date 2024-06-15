import { modes, type ModeComponentProps } from '.';
import { z } from 'zod';

/**
 * The name of a mode
 */
export type Name = keyof typeof modes;

export type ComputedData<M extends Name = Name> = z.infer<(typeof modes)[M]['computedFileData']>;
export type GetComputedData<M extends Name = Name> = ModeComponentProps<M>['getComputedData'];
export type ModeState<M extends Name = Name> = z.infer<(typeof modes)[M]['modeState']>;
export type FileState<M extends Name> = z.infer<(typeof modes)[M]['fileState']>;
