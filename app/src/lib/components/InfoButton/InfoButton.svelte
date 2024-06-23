<script lang="ts">
	import * as Dialog from '$lib/components/ui/dialog';
	import * as Accordion from '$lib/components/ui/accordion/index.js';
	import { Button } from '../ui/button';
	import { contents } from '.';
	import { CircleHelpIcon } from 'lucide-svelte';
	import * as Tooltip from '$lib/components/ui/tooltip';
</script>

<Dialog.Root>
	<Tooltip.Root openDelay={200}>
		<Dialog.Trigger class="h-fit">
			<Tooltip.Trigger asChild let:builder>
				<Button builders={[builder]} variant="ghost">
					Help <CircleHelpIcon class="ml-2" />
				</Button>
			</Tooltip.Trigger>
			<Tooltip.Content>
				<p class="w-36 text-center">Help about what each mode of analysis does</p>
			</Tooltip.Content>
		</Dialog.Trigger>
	</Tooltip.Root>

	<Dialog.Content>
		<Accordion.Root>
			<h1 class="text-3xl font-bold">Help</h1>
			{#each contents as content}
				<Accordion.Item value={content.title}>
					<Accordion.Trigger>{content.title}</Accordion.Trigger>
					<Accordion.Content>
						<svelte:component this={content.content} />
					</Accordion.Content>
				</Accordion.Item>
			{/each}
		</Accordion.Root>
	</Dialog.Content>
</Dialog.Root>
