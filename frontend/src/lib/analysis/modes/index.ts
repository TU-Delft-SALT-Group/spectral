import type { ComponentType } from 'svelte';

import { simpleInfoData, SimpleInfo } from './simple-info';
import { waveformData, Waveform } from './waveform';

import AudioWaveformIcon from 'lucide-svelte/icons/audio-waveform';
import InfoIcon from 'lucide-svelte/icons/info';
import { z } from 'zod';
import { Spectrogram, SpectrogramIcon, spectrogramData } from './spectrogram';

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
	 * The name of the file
	 */
	name: string;
}

export const modeDataValidator = z.union([simpleInfoData, waveformData, spectrogramData]);

/**
 * Data for a specific mode of analysis.
 *
 * This type is a union of all possible modes of analysis. Each mode has a different set of fields.
 */
export type ModeData = z.infer<typeof modeDataValidator> & BaseModeData;

/**
 * List of all the mode names/ids. It would be nice to autogenerate this from `ModeData`, but that is currently not possible in TypeScript (https://stackoverflow.com/questions/44480644/string-union-to-string-array).
 *
 * We do have the guarantee that every entry of `modes` is a valid mode of `ModeData`. However, I haven't found a way to do the oppossite (i.e., the code compiles even if `modes` doesn't contain all modes of `ModeData`).
 */
export const modes = ['simple-info', 'waveform', 'spectrogram'] as const satisfies Array<
	ModeData['mode']
>;

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
	switch (mode) {
		case 'simple-info':
			return SimpleInfo;
		case 'waveform':
			return Waveform;
		case 'spectrogram':
			return Spectrogram;
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
		case 'spectrogram':
			return SpectrogramIcon;
	}
}
