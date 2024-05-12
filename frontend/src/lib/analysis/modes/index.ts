import type { ComponentType } from 'svelte';

import SimpleInfo from './simple-info/SimpleInfo.svelte';
import Waveform from './waveform/Waveform.svelte';
import Unimplemented from './Unimplemented.svelte';

import type { Icon } from 'lucide-svelte';
import AudioWaveformIcon from 'lucide-svelte/icons/audio-waveform';
import CircleHelpIcon from 'lucide-svelte/icons/circle-help';
import InfoIcon from 'lucide-svelte/icons/info';

export type Mode = ModeData['mode'];

export interface BaseModeData {
	/**
	 * The mode of analysis
	 */
	mode: string;

	/**
	 * The unique id of this file
	 */
	fileId: string;

	/**
	 * The size of the file, in bytes
	 */
	fileSize: number;
}

/**
 * Data for a specific mode of analysis.
 *
 * This type is a union of all possible modes of analysis. Each mode has a different set of fields.
 */
export type ModeData = (
	| {
			mode: 'simple-info';

			/**
			 * The duration of the audio file
			 */
			duration: number;
	  }
	| {
			mode: 'waveform';
	  }
	| {
			mode: 'spectogram';
	  }
	| {
			mode: 'vowel-space';
	  }
	| {
			mode: 'transcription';
	  }
	| {
			mode: 'automatic-speech-recognition';
	  }
) &
	BaseModeData;

/**
 * List of all the mode names/ids. It would be nice to autogenerate this from `ModeData`, but that is currently not possible in TypeScript (https://stackoverflow.com/questions/44480644/string-union-to-string-array).
 *
 * We do have the guarantee that every entry of `modes` is a valid mode of `ModeData`. However, I haven't found a way to do the oppossite (i.e., the code compiles even if `modes` doesn't contain all modes of `ModeData`).
 */
export const modes = [
	'simple-info',
	'waveform',
	'spectogram',
	'vowel-space',
	'transcription',
	'automatic-speech-recognition'
] as const satisfies Array<ModeData['mode']>;

/**
 * Helper type to get the specific type of data for a mode
 *
 * @example
 * ```ts
 * type WaveformData = SpecificModeData<'waveform'>;
 * ```
 */
export type SpecificModeData<Mode> = ModeData & { mode: Mode };

export function getComponent(mode: Mode): ComponentType {
	console.log('mode:', mode);

	switch (mode) {
		case 'simple-info':
			return SimpleInfo;
		case 'waveform':
			return Waveform;
		default:
			return Unimplemented;
	}
}

// TODO: Return type should be `ComponentType<Icon>`, but it is currently broken:
// https://github.com/lucide-icons/lucide/pull/2119
export function getIcon(mode: Mode): ComponentType {
	switch (mode) {
		case 'simple-info':
			return InfoIcon;
		case 'waveform':
			return AudioWaveformIcon;
		default:
			return CircleHelpIcon;
	}
}
