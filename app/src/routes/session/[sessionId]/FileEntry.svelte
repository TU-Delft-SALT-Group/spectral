<script lang="ts">
	import { Button } from '$lib/components/ui/button';
	import * as ContextMenu from '$lib/components/ui/context-menu';
	import { invalidateAll } from '$app/navigation';
	import { FileIcon } from 'lucide-svelte';
	import type { FileState } from '$lib/analysis/modes/file-state';

	export let file: FileState;

	// Manual fetch because it's a hassle to set up the form
	async function deleteFile(fileId: string) {
		await fetch('?/deleteFile', { method: 'POST', body: JSON.stringify({ fileId }) });
		await invalidateAll();
	}
</script>

<ContextMenu.Root>
	<ContextMenu.Trigger>
		<Button class="flex-2 w-full justify-start gap-2 rounded" variant="ghost">
			<FileIcon class="h-6 w-6"></FileIcon>
			<span class="overflow-hidden text-ellipsis">
				{file.name}
			</span>
		</Button>
	</ContextMenu.Trigger>

	<ContextMenu.Content>
		<ContextMenu.Item on:click={() => deleteFile(file.id)}>
			<span> Delete </span>
		</ContextMenu.Item>
	</ContextMenu.Content>
</ContextMenu.Root>
