<script lang="ts" context="module">
	import { Button } from '$lib/components/ui/button';
	import { FileIcon, FolderIcon } from 'lucide-svelte';
	import type { ComponentType } from 'svelte';

	type Filetype = 'file' | 'folder';
	export type File = {
		name: string;
		type: Filetype;
	};

	function getFileIcon(type: Filetype): ComponentType {
		switch (type) {
			case 'file':
				return FileIcon;
			case 'folder':
				return FolderIcon;
		}
	}
</script>

<!--
	@component

	File explorer for the audio files. 
-->

<script lang="ts">
	export let files: File[];
</script>

<div class="h-full w-64 bg-red-800">
	<ol>
		{#each files as file}
			<li>
				<Button class="flex-2 flex w-full justify-start gap-2 rounded-none">
					<svelte:component this={getFileIcon(file.type)}></svelte:component>
					<span>
						{file.name}
					</span>
				</Button>
			</li>
		{/each}
	</ol>
</div>
