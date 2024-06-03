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
	class="flex h-full w-full items-center justify-center bg-secondary text-secondary-foreground"
>
	To create a new tab

	<Button class="ml-2" variant="outline" onclick={onClick}>Click here</Button>
</section>
