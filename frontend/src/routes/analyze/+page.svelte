<script lang="ts">
	import FileExplorer, { type File } from './FileExplorer.svelte';
	import NavBar from './NavBar.svelte';
	import Workspace from './Workspace.svelte';

	// TODO: Remove example
	const filesExample = [
		{ name: 'hello', type: 'file' },
		{ name: 'world', type: 'file' },
		{ name: 'homework', type: 'folder' }
	] satisfies File[];
</script>

<main class="grid h-screen w-screen grid-rows-[auto_2fr]">
	<NavBar></NavBar>

	<div class="h-full flex">
		<FileExplorer files={filesExample}></FileExplorer>
		<Workspace></Workspace>
	</div>
</main>
