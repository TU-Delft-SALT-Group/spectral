<script lang="ts">
	import type { PageServerData } from './$types';
	import FileExplorer from './FileExplorer.svelte';
	import Workspace from './Workspace.svelte';

	export let data: PageServerData;
</script>

<div class="grid h-full w-screen grid-cols-[auto,1fr]">
	<FileExplorer files={data.files}></FileExplorer>
	<Workspace bind:state={data.state}></Workspace>
</div>
