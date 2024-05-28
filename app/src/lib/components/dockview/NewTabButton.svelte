<script lang="ts">
	import type { DockviewApi } from 'dockview-core';
	import { Button } from '../ui/button';
	import used from '$lib/utils';

	export let containerApi: DockviewApi;
	export let defaultProps: Record<string, unknown>;

	function onClick(event: MouseEvent) {
		used(event);
		containerApi.addPanel({
			component: 'lmao',
			id: 'added!',
			params: defaultProps
		});
	}
</script>

<Button
	class="bg-panes h-full rounded-none px-2 text-panes-color"
	variant="ghost"
	on:click={onClick}>+</Button
>
