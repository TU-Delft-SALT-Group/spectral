<script
	setup
	lang="ts"
	generics="
	S extends Record<string, unknown>
"
>
	import Watermark from './Watermark.svelte';

	import { paneState } from '$lib/analysis/analysis-pane';

	import { error } from '@sveltejs/kit';
	import {
		DockviewApi,
		DockviewComponent,
		type DockviewOptions,
		type DockviewFrameworkOptions,
		type DockviewReadyEvent
	} from 'dockview-core';
	import { type SvelteComponent, onDestroy, onMount, type ComponentType } from 'svelte';
	import { SvelteRenderer, SvelteTabActionRenderer, SvelteWatermarkRenderer } from '.';
	import used from '$lib/utils';
	import NewTabButton from './NewTabButton.svelte';
	import Tab from './Tab.svelte';

	export let onReady: (event: DockviewReadyEvent) => void;
	// eslint-disable-next-line
	export let component: ComponentType<SvelteComponent<S>>;

	let el: HTMLElement;
	let instance: DockviewComponent | null;

	onMount(() => {
		if (!el) {
			throw error(500, 'element is not mounted');
		}

		const options: DockviewOptions = {};

		const frameworkOptions: DockviewFrameworkOptions = {
			parentElement: el,
			createComponent(options) {
				used(options);
				return new SvelteRenderer(component);
			},
			createLeftHeaderActionComponent(group) {
				return new SvelteTabActionRenderer(NewTabButton, group, {
					state: paneState.parse(undefined)
				});
			},
			createTabComponent(options) {
				used(options);
				return new SvelteRenderer(Tab);
			},
			createWatermarkComponent() {
				return new SvelteWatermarkRenderer(Watermark, {
					state: paneState.parse(undefined)
				});
			}
		};

		const dockview = new DockviewComponent({
			...options,
			...frameworkOptions
		});

		const { clientWidth, clientHeight } = el;
		dockview.layout(clientWidth, clientHeight);

		instance = dockview;

		onReady({ api: new DockviewApi(dockview) });
	});

	onDestroy(() => {
		if (instance !== null) {
			instance?.dispose();
		}
	});
</script>

<section bind:this={el} class="dockview-theme-dark h-full w-full"></section>

<style>
	:global(section.dockview-theme-dark) {
		--dv-tabs-and-actions-container-height: theme(space.8);
		--dv-group-view-background-color: theme(colors.background);
		--dv-tabs-and-actions-container-background-color: theme(colors.secondary.DEFAULT / 50%);
		--dv-activegroup-visiblepanel-tab-background-color: theme(colors.secondary.DEFAULT / 50%);
		--dv-background-color: theme(colors.secondary.DEFAULT);
	}
</style>
