import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  tutorialSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Module 1: ROS Foundations',
      link: {
        type: 'generated-index',
        slug: '/module-1-ros-foundations',
      },
      items: [
          'module-1-ros-foundations/chapter-1',
          'module-1-ros-foundations/chapter-2',
      ],
    },
    {
      type: 'category',
      label: 'Module 2: Nodes, Topics, Services',
      link: {
        type: 'generated-index',
        slug: '/module-2-nodes-topics-services',
      },
      items: [
          'module-2-nodes-topics-services/chapter-1',
          'module-2-nodes-topics-services/chapter-2',
      ],
    },
    {
      type: 'category',
      label: 'Module 3: URDF & Humanoid Simulation',
      link: {
        type: 'generated-index',
        slug: '/module-3-urdf-humanoid-simulation',
      },
      items: [
          'module-3-urdf-humanoid-simulation/chapter-1',
          'module-3-urdf-humanoid-simulation/chapter-2',
      ],
    },
    {
        type: 'category',
        label: 'Module 4: Perception & SLAM',
        link: {
            type: 'generated-index',
            slug: '/module-4-perception-slam',
        },
        items: [
            'module-4-perception-slam/chapter-1',
            'module-4-perception-slam/chapter-2',
        ],
    },
    {
        type: 'category',
        label: 'Module 5: Navigation & Manipulation',
        link: {
            type: 'generated-index',
            slug: '/module-5-navigation-manipulation',
        },
        items: [
            'module-5-navigation-manipulation/chapter-1',
            'module-5-navigation-manipulation/chapter-2',
        ],
    },
    {
        type: 'category',
        label: 'Module 6: Vision, Language & Action',
        link: {
            type: 'generated-index',
            slug: '/module-6-vision-language-action',
        },
        items: [
            'module-6-vision-language-action/chapter-1',
            'module-6-vision-language-action/chapter-2',
        ],
    },
    'capstone-project/capstone-project',
  ],
};

export default sidebars;


export default sidebars;
