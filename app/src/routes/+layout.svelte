<script lang="ts">
	import 'dockview-core/dist/styles/dockview.css';
	import '../app.pcss';

	import { ModeWatcher } from 'mode-watcher';
	import Menubar from './Menubar.svelte';
</script>

<ModeWatcher></ModeWatcher>

<main class="grid h-screen w-screen grid-rows-[auto_2fr] overflow-x-hidden">
	<Menubar></Menubar>
	<div class="overflow-none h-full">
		<slot></slot>
	</div>
</main>

<style>
</style>
