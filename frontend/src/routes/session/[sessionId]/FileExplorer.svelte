<!--
	@component

	File explorer for the audio files. 
-->

<script lang="ts">
	import { Button } from '$lib/components/ui/button';
	import { getFileIcon, type File } from '$lib/files';

	export let files: File[];
</script>

<div class="h-full w-64 bg-secondary">
	<ol>
		{#each files as file}
			<li>
				<Button class="flex-2 flex w-full justify-start gap-2 rounded-none" variant="default">
					<svelte:component this={getFileIcon(file.type)}></svelte:component>
					<span>
						{file.name}
					</span>
				</Button>
			</li>
		{/each}
	</ol>
</div>
