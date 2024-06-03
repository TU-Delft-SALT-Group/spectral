<script lang="ts">
	import type { DockviewApi, IDockviewGroupPanel } from 'dockview-core';
	import { Button } from '../ui/button';
	import { generateIdFromEntropySize } from 'lucia';
	import type { PaneState } from '$lib/analysis/analysis-pane';

	export let containerApi: DockviewApi;
	export let defaultProps: { state: PaneState };
	export let group: IDockviewGroupPanel | undefined;

	function onClick(event: MouseEvent) {
		event.preventDefault();

		containerApi.addPanel({
			component: 'default',
			id: generateIdFromEntropySize(10),
			title: defaultProps.state.title,
			renderer: 'always',
			params: defaultProps,
			position: group === undefined ? undefined : { referenceGroup: group.id },
			tabComponent: 'non default'
		});
	}
</script>

<section
	class="flex h-full w-full flex-col items-center justify-center bg-secondary text-secondary-foreground"
>
	<div class="pb-4 text-muted-foreground">You have no tabs opened</div>

	<Button class="ml-2 px-8 py-4 text-xl" variant="default" onclick={onClick}>New tab</Button>
</section>
