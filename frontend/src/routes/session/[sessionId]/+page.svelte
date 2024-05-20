<script lang="ts">
	import * as Resizable from '$lib/components/ui/resizable';
	import type { PageServerData } from './$types';
	import FileExplorer from './FileExplorer.svelte';
	import Workspace from './Workspace.svelte';

	export let data: PageServerData;
</script>

<div class="flex h-full">
	<Resizable.PaneGroup direction="horizontal">
		<Resizable.Pane defaultSize={20} minSize={11}>
			<FileExplorer files={data.files} sessionId={data.sessionId}></FileExplorer>
		</Resizable.Pane>

		<Resizable.Handle withHandle />

		<Resizable.Pane defaultSize={80}>
			<Workspace bind:state={data.state}></Workspace>
		</Resizable.Pane>
	</Resizable.PaneGroup>
</div>
