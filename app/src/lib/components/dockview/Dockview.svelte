<script
	setup
	lang="ts"
	generics="
	S extends Record<string, unknown> & { title?: string }
"
>
	import Watermark from './Watermark.svelte';

	import { error } from '@sveltejs/kit';
	import {
		DockviewApi,
		DockviewComponent,
		type DockviewOptions,
		type DockviewFrameworkOptions,
		type DockviewReadyEvent
	} from 'dockview-core';
	import { type SvelteComponent, onDestroy, onMount, type ComponentType } from 'svelte';
	import { SvelteRenderer, SvelteTabActionRenderer, SvelteWatermarkRenderer } from './index.svelte';
	import NewTabButton from './NewTabButton.svelte';
	import Tab from './Tab.svelte';

	type Component<T extends Record<string, unknown>> = ComponentType<SvelteComponent<T>>;

	let {
		onReady,
		component,
		getDefaultProps
	}: {
		// eslint-disable-next-line
		component: Component<S>;
		onReady: (event: DockviewReadyEvent) => void;
		// eslint-disable-next-line
		getDefaultProps: () => S;
	} = $props();

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
				return new SvelteRenderer(component, options);
			},
			createLeftHeaderActionComponent(group) {
				// eslint-disable-next-line
				return new SvelteTabActionRenderer<S>(NewTabButton, group, getDefaultProps);
			},
			createTabComponent(options) {
				return new SvelteRenderer(Tab, options);
			},
			createWatermarkComponent() {
				// eslint-disable-next-line
				return new SvelteWatermarkRenderer<S>(Watermark, getDefaultProps);
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

<section bind:this={el} class="dockview-theme-dark dockview-custom h-full w-full"></section>

<style>
	:global(section.dockview-custom) {
		/* Unknown */
		/* --dv-paneview-active-outline-color: theme(colors.lime.500); */

		--dv-tabs-and-actions-container-font-size: 0.8rem;
		--dv-tabs-and-actions-container-height: theme(space.8);

		/* Probably not necessary for us */
		/* --dv-tab-close-icon: ; */

		--dv-drag-over-background-color: theme(colors.primary.DEFAULT / 20%);

		/* Unknown */
		--dv-drag-over-border-color: theme(colors.red.500);

		/* Not sure when it appears */
		--dv-tabs-container-scrollbar-color: theme(colors.primary.DEFAULT);

		--dv-group-view-background-color: theme(colors.background);

		/* Unknown */
		--dv-tabs-and-actions-container-background-color: theme(colors.secondary.DEFAULT / 20%);
		--dv-tabs-and-actions-container-background-color: theme(colors.secondary.DEFAULT);

		--dv-activegroup-visiblepanel-tab-background-color: theme(colors.background);
		--dv-activegroup-hiddenpanel-tab-background-color: theme(colors.secondary.DEFAULT / 20%);

		--dv-inactivegroup-visiblepanel-tab-background-color: theme(colors.background);
		--dv-inactivegroup-hiddenpanel-tab-background-color: theme(colors.secondary.DEFAULT / 50%);

		--dv-tab-divider-color: theme(colors.secondary.DEFAULT);

		--dv-activegroup-visiblepanel-tab-color: theme(colors.foreground);
		--dv-activegroup-hiddenpanel-tab-color: theme(colors.secondary.foreground / 70%);
		--dv-inactivegroup-visiblepanel-tab-color: theme(colors.secondary.foreground / 70%);
		--dv-inactivegroup-hiddenpanel-tab-color: theme(colors.secondary.foreground / 40%);

		--dv-separator-border: theme(colors.accent.DEFAULT);

		/* Unknown */
		--dv-paneview-header-border-color: theme(colors.secondary.DEFAULT);

		/* Probably not used? */
		/* --dv-icon-hover-background-color	 */
		/* --dv-floating-box-shadow	 */
		/* --dv-active-sash-color	 */

		--dv-background-color: theme(colors.secondary.DEFAULT);
	}

	/* Remove an outline when selecting tab */
	:global(.tab::after) {
		--dv-tab-divider-color: theme(colors.background);
	}
</style>
