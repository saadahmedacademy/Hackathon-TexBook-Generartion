import React from 'react';
import { render, screen } from '@testing-library/react';
import HomepageHeader from './HomepageHeader';

describe('HomepageHeader', () => {
  it('renders the header with the correct text', () => {
    render(<HomepageHeader />);
    expect(screen.getByText('ROS 2 Textbook')).toBeInTheDocument();
    expect(screen.getByText('A comprehensive guide to ROS 2 and humanoid robotics')).toBeInTheDocument();
  });
});
