import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';

import styles from './index.module.css';

// Data for the module cards
const modules = [
  {
    title: 'Module 1: ROS Foundations',
    link: '/docs/module-1-ros-foundations/',
    description: 'Learn about the fundamentals of ROS 2, setting up your environment, and creating your first nodes.',
  },
  {
    title: 'Module 2: Nodes, Topics & Services',
    link: '/docs/module-2-nodes-topics-services/',
    description: 'Explore the core communication mechanisms in ROS 2 that allow different parts of a robot to communicate.',
  },
  {
    title: 'Module 3: URDF & Humanoid Simulation',
    link: '/docs/module-3-urdf-humanoid-simulation/',
    description: 'Learn about robot modeling using URDF and how to simulate humanoid robots in Gazebo.',
  },
  {
    title: 'Module 4: Perception & SLAM',
    link: '/docs/module-4-perception-slam/',
    description: 'Understand how robots perceive their environment using sensors and build maps with SLAM.',
  },
  {
    title: 'Module 5: Navigation & Manipulation',
    link: '/docs/module-5-navigation-manipulation/',
    description: 'Enable robots to move autonomously and interact with objects using Navigation2 and MoveIt2.',
  },
  {
    title: 'Module 6: Vision, Language & Action',
    link: '/docs/module-6-vision-language-action/',
    description: 'Explore advanced topics in robotics, including AI, computer vision, and human-robot interaction.',
  },
];

function ProjectHero() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero', styles.heroBanner)}>
      <div className="container">
        <img
          alt="ROS 2 Textbook Logo"
          src={'img/logo.svg'}
          className={styles.heroLogo}
        />
        <Heading as="h1" className="hero__title">
          {siteConfig.title}
        </Heading>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className="button button--primary button--lg"
            to="/docs/intro">
            Start Reading
          </Link>
        </div>
      </div>
    </header>
  );
}

function ModuleCards() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {modules.map((module, idx) => (
            <div key={idx} className={clsx('col col--4', styles.featureCard)}>
              <div className="card">
                <div className="card__header">
                  <Heading as="h3">{module.title}</Heading>
                </div>
                <div className="card__body">
                  <p>{module.description}</p>
                </div>
                <div className="card__footer">
                  <Link
                    className="button button--secondary button--block"
                    to={module.link}>
                    Explore Module
                  </Link>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

export default function Home(): React.ReactElement {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title="Home"
      description="A comprehensive, open-source guide to ROS 2 for humanoid robotics.">
      <ProjectHero />
      <main>
        <ModuleCards />
      </main>
    </Layout>
  );
}