var goldenlayout_config = {
    content: [{
        type: 'column',
        content: [{
            type: 'row',
            content: [{
                type: 'column',
                width: 75,
                content: [{
                    type: 'component',
                    componentName: 'Main',
                    isClosable: false,
                    tooltip: 'Main - Drag to desired position.',
                    componentState: {
                        cssClass: 'content',
                        types: 'untagged',
                        updateMethod: 'newlines',
                    },
                }, {
                    type: 'component',
                    componentName: 'input',
                    id: 'inputComponent',
                    height: 10,
                    tooltip: 'This cannot be closed or moved.',
                }, ]
            },{
                type: 'column',
                width: 25,
                content: [{
                    type: 'component',
                    componentName: 'evennia',
                    componentId: 'evennia',
                    title: 'Map',
                    height: 60,
                    tooltip: 'Map - Drag to desired position.',
                    isClosable: false,
                    componentState: {
                        types: 'map',
                        updateMethod: 'replace',
                    },
                }, {
                    type: 'component',
                    componentName: 'evennia',
                    componentId: 'evennia',
                    title: 'Inventory',
                    tooltip: 'Inventory - Cannot be closed or moved.',
                    isClosable: false,
                    componentState: {
                        types: 'inventory',
                        updateMethod: 'replace',
                    },
                }],
            }],
        }]
    }]
};