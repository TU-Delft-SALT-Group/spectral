import { z } from 'zod';
import { fileState } from '../file-state';
import type { ModeValidator } from '..';
import BasePlugin, { type BasePluginEvents } from 'wavesurfer.js/dist/base-plugin.js';
import { mount, unmount, type ComponentType, type SvelteComponent } from 'svelte';
import Tracks from './Tracks.svelte';

export { default as Transcription } from './Transcription.svelte';
export { default as TranscriptionIcon } from './TranscriptionIcon.svelte';

export const transcriptionData = {
	computedFileData: z.null(),

	fileState: fileState
		.pick({
			id: true
		})
		.default({}),

	modeState: z.object({}).default({})
} satisfies ModeValidator;

export type Track = {
	captions?: number[]; // TODO: change to correct type later,
};

export type TracksPluginOptions = {
	tracks: Track[];
};

const defaultOptions: TracksPluginOptions = {
	tracks: []
};

type TracksPluginEvents = BasePluginEvents;
type Component<T extends Record<string, unknown>> = ComponentType<SvelteComponent<T>>;

export class TracksPlugin extends BasePlugin<TracksPluginEvents, TracksPluginOptions> {
	protected options: TracksPluginOptions;
	private instance: Component<{ tracks: Track[] }> | null;
	private tracksElement: HTMLElement;
	private props: { tracks: Track[] };

	constructor(options?: TracksPluginOptions) {
		super(options || { tracks: [] });

		this.options = Object.assign({}, defaultOptions, options);
		this.tracksElement = this.initElement();
		this.props = { tracks: [] };
		this.instance = null;
	}

	public static create(options?: TracksPluginOptions): TracksPlugin {
		return new TracksPlugin(options);
	}

	onInit(): void {
		if (!this.wavesurfer) {
			throw Error('Tried to initialize tracks before wavesurfer.');
		}

		const container = this.wavesurfer.getWrapper();
		container.parentNode?.appendChild(this.tracksElement);

		this.subscriptions.push(this.wavesurfer.on('redraw', () => this.redraw()));
	}

	private initElement(): HTMLElement {
		const elem = document.createElement('div');
		elem.style.width = '100%';
		return elem;
	}

	private mount(): void {
		this.instance = mount(Tracks, {
			target: this.tracksElement,
			props: this.props
		}) as Component<{ tracks: Track[] }>;
	}

	private unmount(): void {
		if (this.instance !== null) {
			unmount(this.instance);
		}
	}

	private redraw(): void {
		this.unmount();
		this.mount();
	}

	public update(options: TracksPluginOptions) {
		this.options = { ...this.options, ...options };

		this.props = { tracks: [...this.props.tracks, {}] };
		// TODO: find a change for this
		this.redraw();
	}

	destroy(): void {
		this.unmount();
		super.destroy();
	}
}
