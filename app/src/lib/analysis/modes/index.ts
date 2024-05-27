import type { ComponentType, SvelteComponent } from 'svelte';

import { simpleInfoData, SimpleInfo } from './simple-info';
import { waveformData, Waveform } from './waveform';
import { spectrogramData, Spectrogram, SpectrogramIcon } from './spectrogram';
import { vowelSpaceData, VowelSpace, VowelSpaceIcon } from './vowel-space';
import { errorRateData, ErrorRate } from './error-rate';

import AudioWaveformIcon from 'lucide-svelte/icons/audio-waveform';
import InfoIcon from 'lucide-svelte/icons/info';
import { ZodDefault, ZodSchema } from 'zod';

import type * as mode from './types';
export type * as mode from './types';

export type ModeValidator = {
	/**
	 * Data that is computed from the audio file, given a file id and possibly a frame
	 */
	computedFileData: ZodSchema<unknown>;

	/**
	 * State associated with the mode.
	 *
	 * This state is per-mode on a pane, meaning it doesn't depend on the file.
	 */
	modeState: ZodDefault<ZodSchema<unknown>>;

	/**
	 * State associated with files.
	 *
	 * This state is shared between all modes, meaning that if you set a value `foo` in
	 * one mode, another mode can use that `foo` value. Keep in mind that these values
	 * should be of the same type.
	 */
	fileState: ZodDefault<ZodSchema<unknown>>;
};

/**
 * The mode data and state schemas, necessary for the renderer to display the mode
 *
 * The data is the information that can be computed from the audio.
 *
 * The state is composed of extra parameters that the user sets which control the renderer.
 * In other words, the state is the configuration of the renderer, or the necessary info that
 * is not computed from the audio.
 *
 * Here you register modes. When adding a new mode, you also need to update the `modeComponents`
 * record.
 *
 * It would be nice for that to be included here, but I have not found a way to strongly type
 * object properties based on sibling properties.
 */
export const modes = {
	'simple-info': simpleInfoData,
	waveform: waveformData,
	spectrogram: spectrogramData,
	'vowel-space': vowelSpaceData,
	'error-rate': errorRateData
} as const satisfies Record<string, ModeValidator>;

/**
 * The names of the modes
 *
 * This helper is useful because `Object.keys(modes)` returns a `string[]` instead of a `Mode.Name[]`.
 */
export const modeNames: mode.Name[] = Object.keys(modes) as Array<keyof typeof modes>;

export type FileData<M extends mode.Name> = {
	computedData: mode.ComputedData<M>;
	fileState: mode.FileState<M>;
};

export type ModeComponentProps<M extends mode.Name> = {
	fileData: Array<FileData<M>>;
	modeState: mode.ModeState<M>;
	onRemoveFile?: (fileId: string) => void;
};

export type ModeComponent<M extends mode.Name> = ComponentType<
	SvelteComponent<ModeComponentProps<M>>
>;

/**
 * The components that render the modes.
 *
 * Modes are registered in the `modes` record.
 */
export const modeComponents: {
	[M in keyof typeof modes]: {
		component: ModeComponent<M>;
		icon: ComponentType;
	};
} = {
	'simple-info': {
		component: SimpleInfo,
		icon: InfoIcon
	},

	waveform: {
		component: Waveform,
		icon: AudioWaveformIcon
	},

	spectrogram: {
		component: Spectrogram,
		icon: SpectrogramIcon
	},

	'vowel-space': {
		component: VowelSpace,
		icon: VowelSpaceIcon
	},

	'error-rate': {
		component: ErrorRate,
		icon: InfoIcon
	}
};
