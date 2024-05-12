<script lang="ts">
	import type { PageServerData } from './$types';
	import FileExplorer from './FileExplorer.svelte';
	import Workspace from './Workspace.svelte';

	export let data: PageServerData;
</script>

<div class="flex h-full">
	<FileExplorer files={data.files}></FileExplorer>
	<Workspace bind:state={data.state}></Workspace>
</div>
