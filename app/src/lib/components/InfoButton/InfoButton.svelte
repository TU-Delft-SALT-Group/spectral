<script lang="ts">
	import * as Dialog from '$lib/components/ui/dialog';
	import * as Accordion from '$lib/components/ui/accordion/index.js';
	import { Button } from '../ui/button';
	import { contents } from '.';
</script>

<Dialog.Root>
	<Dialog.Trigger>
		<!-- TODO: Change it to a better phrase -->
		<Button variant="ghost">Show Info</Button>
	</Dialog.Trigger>

	<Dialog.Content>
		<Accordion.Root>
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
