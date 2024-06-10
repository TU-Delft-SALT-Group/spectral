<script
	lang="ts"
	generics="
	S extends Record<string, unknown> & { title?: string }
"
>
	import type { DockviewApi, IDockviewGroupPanel } from 'dockview-core';
	import { Button } from '../ui/button';
	import { generateIdFromEntropySize } from 'lucia';

	export let group: IDockviewGroupPanel;
	export let containerApi: DockviewApi;
	// eslint-disable-next-line
	export let defaultProps: S;

	function onClick(event: MouseEvent) {
		event.preventDefault();

		containerApi.addPanel({
			component: 'default',
			id: generateIdFromEntropySize(10),
			title: defaultProps.title ?? 'default',
			renderer: 'always',
			params: defaultProps,
			position: { referenceGroup: group.id },
			tabComponent: 'non default'
		});
	}
</script>

<Button
	class="bg-panes text-panes-color h-full rounded-none px-2"
	variant="ghost"
	on:click={onClick}>+</Button
>
