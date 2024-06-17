<script lang="ts" generics="S extends Record<string, unknown> & { title?: string}">
	import type { DockviewApi, IDockviewGroupPanel } from 'dockview-core';
	import { Button } from '../ui/button';
	import { generateIdFromEntropySize } from 'lucia';

	export let containerApi: DockviewApi;
	// eslint-disable-next-line
	export let defaultProps: () => S;
	export let group: IDockviewGroupPanel | undefined;

	function onClick(event: MouseEvent) {
		event.preventDefault();

		const props = defaultProps();

		containerApi.addPanel({
			component: 'default',
			id: generateIdFromEntropySize(10),
			title: props.title ?? 'default',
			renderer: 'always',
			params: props,
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
