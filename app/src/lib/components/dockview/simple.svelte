<script lang="ts">
	import type { ComponentProps } from '.';

	let { params }: ComponentProps = $props();
</script>

<div>{params.params.content}</div>
