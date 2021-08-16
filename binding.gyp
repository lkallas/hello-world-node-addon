{
  'targets': [
    {
      'target_name': 'hello-world',
      'sources': [ 'hello_world.cc' ],
      'conditions': [
        [
          'OS=="win"',
          {
            'actions': [
              {
                'action_name': 'hello_world_python',
                'inputs': [
                  'deps/hello-world.py'
                ],
                'outputs': ['deps/fake.out'],
                'message': 'Running "Hello world" from Python!',
                'action': ['python', '<@(_inputs)']
              }
            ]
          }
        ]
      ]
    }
  ]
}
