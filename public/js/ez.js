/// <reference path="./node_modules/@types/react/index.d.ts" />

const exampleElement = {
    type: 'div',
    props: null,
    children: [
        {
            type: 'h1',
            props: null,
            children: 'Hello, world!'
        },
        {
            type: 'p',
            props: null,
            children: 'This is a test of the createElement function'
        }
    ]
}

class Ez {
    #ezReactRootNode = ReactDOM.createRoot(document.getElementById('root'))

    #convertToReact(element) {
        if (typeof element === 'string') {
            return element;
        }
        const children = Array.isArray(element.children) ? element.children.map((v) => this.#convertToReact(v)) : [element.children];
        return React.createElement(element.type, element.props, ...children);
    }

    get reactRootNode() {
        return this.#ezReactRootNode;
    }

    render(element) {
        this.#ezReactRootNode.render(this.#convertToReact(element));
    }

    async getComponent(componentName, props = {}) {
        const response = await fetch(`/c/${componentName}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(props)
        });
        return await response.json();
    }
}


async function foo() {
    const ez = new Ez();
    const plugins = await (await fetch('/api/plugins')).json();
    const component = await ez.getComponent('PluginList', { plugins });
    exampleElement.children.push(component)
    ez.render(exampleElement);
}