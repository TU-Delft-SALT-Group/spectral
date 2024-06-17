<script lang="ts">
	import AnalysisPane from '$lib/analysis/AnalysisPane.svelte';
	import { DockviewApi, type DockviewReadyEvent, type SerializedDockview } from 'dockview-core';
	import type { SessionState } from './workspace';
	import Dockview from '$lib/components/dockview/Dockview.svelte';
	import type { SvelteRenderer } from '$lib/components/dockview/index.svelte';
	import type { ComponentType } from 'svelte';
	import { paneState } from '$lib/analysis/analysis-pane';

	let { workspaceState = $bindable() }: { workspaceState: SessionState } = $props();
	let panesApi: DockviewApi;

	const getDefaultProps = () => {
		const defaultState = structuredClone(paneState.parse(undefined));
		const defaultProps = $state(defaultState);

		return {
			title: 'New Tab',
			paneState: defaultProps
		};
	};

	export function deleteFile(fileId: string) {
		for (const pane of panesApi.panels) {
			const instance = pane.view.content as SvelteRenderer;
			(
				instance.getInstance() as (ComponentType & { removeFile: (id: string) => void }) | undefined
			)?.removeFile(fileId);
		}
	}

	function onReady(event: DockviewReadyEvent) {
		panesApi = event.api;

		// since layout is only stored from here, everything should be fine
		let layout = workspaceState.layout as SerializedDockview | undefined;

		if (layout !== undefined) layout.panels = {};

		for (const paneId in workspaceState.panes) {
			const pane = workspaceState.panes[paneId];

			const panel = panesApi.addPanel({
				id: paneId,
				title: pane.title,
				component: 'the panel',
				renderer: 'onlyWhenVisible',
				tabComponent: 'not default',
				params: {
					paneState: workspaceState.panes[paneId]
				}
			});

			if (layout !== undefined) {
				layout.panels[paneId] = panel.toJSON();
			}
		}

		if (layout !== undefined) {
			panesApi.fromJSON(layout);
			for (const panel of panesApi.panels) {
				panel.api.setRenderer('always');
				panel.api.onDidTitleChange((e) => {
					workspaceState.panes[panel.id].title = e.title;
				});
			}
		}

		panesApi.onDidAddPanel((event) => {
			if (event.params === undefined) {
				return;
			}

			workspaceState.panes[event.id] = event.params.paneState;
		});

		panesApi.onDidRemovePanel((event) => {
			if (event.params === undefined) {
				return;
			}

			delete workspaceState.panes[event.id];
		});

		panesApi.onDidLayoutChange(() => {
			workspaceState.layout = panesApi.toJSON();
		});
	}
</script>

<div class="h-full w-full">
	<Dockview {onReady} component={AnalysisPane} {getDefaultProps} />
</div>
