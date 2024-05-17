<script lang="ts">
	import '../app.pcss';

	import { ModeWatcher } from 'mode-watcher';
	import NavBar from './NavBar.svelte';
</script>

<ModeWatcher></ModeWatcher>

<main class="grid h-screen w-screen grid-rows-[auto_2fr] overflow-x-hidden">
	<NavBar></NavBar>
	<div class="overflow-none h-full">
		<slot></slot>
	</div>
</main>
