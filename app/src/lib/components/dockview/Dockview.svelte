<script
	setup
	lang="ts"
	generics="
	S extends Record<string, unknown>
"
>
	import { error } from '@sveltejs/kit';
	import {
		DockviewApi,
		DockviewComponent,
		type DockviewOptions,
		type DockviewFrameworkOptions,
		type DockviewReadyEvent
	} from 'dockview-core';
	import { SvelteComponent, onDestroy, onMount, type ComponentType } from 'svelte';
	import { SvelteRenderer } from '.';
	import used from '$lib/utils';

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

<section bind:this={el} class="dockview-theme-dark h-screen w-screen"></section>
