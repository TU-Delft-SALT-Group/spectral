<script lang="ts">
	import * as Resizable from '$lib/components/ui/resizable';
	import type { PaneGroupAPI } from 'paneforge';
	import { doubleClick, focusOut, keyDown } from '.';

	let {
		captions = $bindable(),
		duration,
		isLast,
		createRegion
	}: {
		captions: Caption[];
		duration: number | null;
		isLast: boolean;
		createRegion: (start: number, end: number) => void;
	} = $props();

	let paneGroup: PaneGroupAPI | undefined = $state(undefined);

	type Caption = {
		start: number;
		end: number;
		value: string;
	};

	function handleCreate(event: MouseEvent, caption: Caption) {
		if (!(event.target instanceof HTMLElement)) {
			throw Error('event target is not a html element');
		}

		if (!event.shiftKey) {
			return;
		}

		const boundingBox = event.target.getBoundingClientRect();
		const percentage = (event.x - boundingBox.left) / boundingBox.width;
		const oldEnd = caption.end;
		const ind = captions.indexOf(caption);

		caption.end = caption.start + (caption.end - caption.start) * percentage;

		let newCaption: Caption = {
			start: caption.end,
			end: oldEnd,
			value: ''
		};

		captions = [...captions.slice(0, ind + 1), newCaption, ...captions.slice(ind + 1)];
	}

	function handleDelete(event: MouseEvent, index: number) {
		if (!event.altKey) {
			return;
		}

		const caption = captions[index];
		const nextCaption = captions[index + 1];
		const newCaption = {
			start: caption.start,
			end: nextCaption.end,
			value: caption.value + nextCaption.value
		};

		captions = [...captions.slice(0, index), newCaption, ...captions.slice(index + 2)];
	}
</script>

<div
	class="flex w-full flex-row items-center gap-4 border-t border-primary/60"
	class:border-b={isLast}
>
	<Resizable.PaneGroup direction="horizontal" class="w-full" bind:paneGroup>
		{#if duration !== null}
			{#each captions as caption, i ([caption.start, caption.end])}
				<Resizable.Pane class="w-full" defaultSize={(caption.start - caption.end) / duration}>
					<span
						role="button"
						tabindex="0"
						class="flex h-full w-full items-center justify-center overflow-clip rounded-none bg-accent text-accent-foreground"
						onclick={(event: MouseEvent) => handleCreate(event, caption)}
						ondblclick={(event: MouseEvent)=>{
							doubleClick(event)
							createRegion(caption.start, caption.end)
						}}
						onfocusout={(event: FocusEvent) => focusOut(event, caption)}
						onkeydown={(event: KeyboardEvent) => keyDown(event, caption)}>{caption.value}</span
					>
				</Resizable.Pane>

				{#if caption !== captions[captions.length - 1]}
					<Resizable.Handle class="bg-primary/20" onclick={(event) => handleDelete(event, i)} />
				{/if}
			{/each}
		{/if}
	</Resizable.PaneGroup>
</div>
