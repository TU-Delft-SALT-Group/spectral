import type {
	DockviewApi,
	DockviewPanelApi,
	GroupPanelPartInitParameters,
	IContentRenderer,
	IDockviewPanelHeaderProps,
	ITabRenderer,
	PanelUpdateEvent,
	Parameters
} from 'dockview-core';

import {
	type SvelteComponent,
	mount,
	unmount,
	type ComponentProps,
	type ComponentType
} from 'svelte';

export function mountComponent<S extends Record<string, unknown>>(
	component: ComponentType<SvelteComponent<S>>,
	props: IDockviewPanelHeaderProps<ComponentProps<SvelteComponent<S>>>,
	element: HTMLElement
) {
	console.log(props.params);
	let mounted = mount(component, {
		target: element,
		props: props.params
	});

	return {
		update: (newProps: object) => {
			mounted = { ...mounted, ...newProps };
		},
		dispose: () => {
			unmount(mounted);
		}
	};
}

abstract class AbstractSvelteRenderer {
	readonly _element: HTMLElement;

	get element() {
		return this._element;
	}

	constructor() {
		this._element = document.createElement('section');
		this.element.className = 'dv-vue-part';
		this.element.style.height = '100%';
		this.element.style.width = '100%';
	}
}

export class SvelteRenderer<S extends Record<string, unknown>>
	extends AbstractSvelteRenderer
	implements IContentRenderer, ITabRenderer
{
	readonly _component: ComponentType<SvelteComponent<S>>;
	private _renderDisposable: { update: (props: object) => void; dispose: () => void } | undefined;
	private _api: DockviewPanelApi | undefined;
	private _containerApi: DockviewApi | undefined;

	constructor(component: ComponentType<SvelteComponent<S>>) {
		super();
		this._component = component;
	}

	init(parameters: GroupPanelPartInitParameters): void {
		this._api = parameters.api;
		this._containerApi = parameters.containerApi;

		const panelHeaderProps: IDockviewPanelHeaderProps<S> = {
			params: parameters.params as S,
			api: parameters.api,
			containerApi: parameters.containerApi
		};

		this._renderDisposable?.dispose();
		this._renderDisposable = mountComponent(this._component, panelHeaderProps, this._element);
	}

	update(event: PanelUpdateEvent<Parameters>): void {
		if (this._api === undefined || this._containerApi === undefined) {
			return;
		}

		const params = event.params;

		this._renderDisposable?.update({
			params: {
				params,
				api: this._api,
				containerApi: this._containerApi
			}
		});
	}

	dispose(): void {
		this._renderDisposable?.dispose();
	}
}
