<script lang="ts">
	import type { DockviewApi, IDockviewGroupPanel } from 'dockview-core';
	import { Button } from '../ui/button';
	import { generateIdFromEntropySize } from 'lucia';
	import type { PaneState } from '$lib/analysis/analysis-pane';

	export let group: IDockviewGroupPanel;
	export let containerApi: DockviewApi;
	export let defaultProps: { state: PaneState };

	function onClick(event: MouseEvent) {
		event.preventDefault();

		containerApi.addPanel({
			component: 'default',
			id: generateIdFromEntropySize(10),
			title: defaultProps.state.title,
			renderer: 'always',
			params: defaultProps,
			position: { referenceGroup: group.id }
		});
	}
</script>

<Button
	class="bg-panes h-full rounded-none px-2 text-panes-color"
	variant="ghost"
	on:click={onClick}>+</Button
>
