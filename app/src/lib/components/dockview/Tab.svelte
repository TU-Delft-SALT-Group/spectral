<script lang="ts">
	import type { DockviewPanelApi } from 'dockview-core';
	import { Button } from '../ui/button';

	export let api: DockviewPanelApi;
	export let title: string | undefined;
	let previousTitle: string | null = null;
	let titleElement: HTMLElement;

	function onClickClose(event: MouseEvent) {
		event.preventDefault();
		api.close();
	}

	function onClickTitle(event: MouseEvent) {
		if (event.detail !== 2 || titleElement.isContentEditable) {
			return;
		}

		previousTitle = titleElement.textContent;
		titleElement.contentEditable = 'true';
		let selection = window.getSelection()!;
		selection.selectAllChildren(titleElement);
	}

	function handleKey(event: KeyboardEvent) {
		if (!titleElement.isContentEditable) {
			return;
		}

		if (event.key === 'Enter') {
			console.log(window.getSelection());
			titleElement.contentEditable = 'false';
			api.setTitle(titleElement.textContent!);
		} else if (event.key === 'Escape') {
			titleElement.textContent = previousTitle;
			titleElement.contentEditable = 'false';
		}
	}

	function unfocus() {
		titleElement.contentEditable = 'false';
	}
</script>

<!-- TODO: limit the amount of character that can be written -->
<!-- TODO: fix the fact that the size doesn't change -->
<Button
	class="flex w-fit min-w-0 flex-row rounded-none p-1"
	on:click={onClickTitle}
	on:keydown={handleKey}
	on:focusout={unfocus}
	variant="ghost"
>
	<button class="flex h-full w-full items-center justify-center focus:outline-transparent">
		<span bind:this={titleElement} class="outline-none">
			{title}
		</span>
	</button>
	<Button
		class="ml-auto h-8 w-8 items-center justify-center rounded-none bg-transparent p-0"
		on:click={onClickClose}
		variant="secondary"
	>
		<svg
			height="11"
			width="11"
			viewBox="0 0 28 28"
			aria-hidden="false"
			focusable="false"
			class="dockview-svg"
			><path
				d="M2.1 27.3L0 25.2L11.55 13.65L0 2.1L2.1 0L13.65 11.55L25.2 0L27.3 2.1L15.75 13.65L27.3 25.2L25.2 27.3L13.65 15.75L2.1 27.3Z"
			></path></svg
		>
	</Button>
</Button>
