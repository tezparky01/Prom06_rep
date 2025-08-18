#!/usr/bin/env python3
"""
Digital Twin EVM Dashboard - Callbacks Module
============================================

All callback functions for interactive charts and visualizations.
Modern, clean implementation with professional styling.

Author: Manus AI
Date: December 2024
Version: 3.0 - Split Architecture
"""

from dash import Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

# Import data and functions from main module
from dashboard_main import (
    app, task_progress, time_series, quality_data, response_df, rework_df, step_performance_df,
    total_budget, total_tasks, project_duration_days, final_ev_traditional, final_ev_quality,
    final_ac, total_rework_cost, final_spi_traditional, final_spi_quality, final_cpi_traditional,
    final_cpi_quality, schedule_variance, cost_variance, total_inspections, pass_count, fail_count,
    offered_count, failure_rate, first_time_right_rate, avg_response_time, avg_rework_time,
    total_quality_delay, first_time_rework_success,
    create_executive_tab, create_detailed_evm_tab, create_quality_tab, create_temporal_tab,
    create_bottleneck_tab, create_task_tab, create_simulation_tab
)

# ============================================================================
# MODERN CHART STYLING
# ============================================================================

# Professional color palette
COLORS = {
    'primary': '#667eea',
    'secondary': '#764ba2',
    'success': '#10b981',
    'warning': '#f59e0b',
    'danger': '#ef4444',
    'info': '#3b82f6',
    'light': '#f8fafc',
    'dark': '#1e293b',
    'muted': '#64748b'
}

# Chart layout template
CHART_LAYOUT = {
    'font': {'family': 'Inter, sans-serif', 'size': 12, 'color': COLORS['dark']},
    'plot_bgcolor': 'white',
    'paper_bgcolor': 'white',
    'margin': {'l': 60, 'r': 40, 't': 60, 'b': 60},
    'showlegend': True,
    'legend': {
        'orientation': 'h',
        'yanchor': 'bottom',
        'y': -0.2,
        'xanchor': 'center',
        'x': 0.5,
        'font': {'size': 11}
    },
    'xaxis': {
        'gridcolor': '#e1e5e9',
        'linecolor': '#e1e5e9',
        'tickfont': {'size': 11, 'color': COLORS['muted']},
        'titlefont': {'size': 12, 'color': COLORS['dark']}
    },
    'yaxis': {
        'gridcolor': '#e1e5e9',
        'linecolor': '#e1e5e9',
        'tickfont': {'size': 11, 'color': COLORS['muted']},
        'titlefont': {'size': 12, 'color': COLORS['dark']}
    }
}

def apply_modern_layout(fig, title="", height=400):
    """Apply modern styling to charts"""
    fig.update_layout(
        **CHART_LAYOUT,
        title={
            'text': title,
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 16, 'weight': 600, 'color': COLORS['dark']}
        },
        height=height
    )
    return fig

# ============================================================================
# MAIN TAB ROUTING
# ============================================================================

@app.callback(Output('tab-content', 'children'),
              Input('main-tabs', 'value'))
def render_tab_content(active_tab):
    """Route to appropriate tab content"""
    tab_map = {
        'executive': create_executive_tab,
        'detailed': create_detailed_evm_tab,
        'quality': create_quality_tab,
        'temporal': create_temporal_tab,
        'bottlenecks': create_bottleneck_tab,
        'tasks': create_task_tab,
        'simulation': create_simulation_tab
    }
    
    if active_tab in tab_map:
        return tab_map[active_tab]()
    else:
        return html.Div([
            html.H3(f"Tab '{active_tab}' not found"),
            html.P("Please select a valid tab.")
        ])

# ============================================================================
# EXECUTIVE TAB CALLBACKS
# ============================================================================

@app.callback(Output('executive-gauges', 'figure'),
              Input('main-tabs', 'value'))
def update_executive_gauges(tab):
    """Performance gauge indicators"""
    fig = make_subplots(
        rows=1, cols=3,
        specs=[[{'type': 'indicator'}, {'type': 'indicator'}, {'type': 'indicator'}]],
        subplot_titles=('Schedule Performance', 'Cost Performance', 'Quality Performance')
    )
    
    # Schedule Performance
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=final_spi_quality,
        title={'text': "SPI", 'font': {'size': 14}},
        gauge={
            'axis': {'range': [None, 1.2], 'tickfont': {'size': 10}},
            'bar': {'color': COLORS['primary']},
            'steps': [
                {'range': [0, 0.8], 'color': '#f1f5f9'},
                {'range': [0.8, 1.0], 'color': '#fef3c7'},
                {'range': [1.0, 1.2], 'color': '#d1fae5'}
            ],
            'threshold': {
                'line': {'color': COLORS['danger'], 'width': 3},
                'thickness': 0.75,
                'value': 1.0
            }
        }
    ), row=1, col=1)
    
    # Cost Performance
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=final_cpi_quality,
        title={'text': "CPI", 'font': {'size': 14}},
        gauge={
            'axis': {'range': [None, 1.2], 'tickfont': {'size': 10}},
            'bar': {'color': COLORS['success']},
            'steps': [
                {'range': [0, 0.8], 'color': '#f1f5f9'},
                {'range': [0.8, 1.0], 'color': '#fef3c7'},
                {'range': [1.0, 1.2], 'color': '#d1fae5'}
            ],
            'threshold': {
                'line': {'color': COLORS['danger'], 'width': 3},
                'thickness': 0.75,
                'value': 1.0
            }
        }
    ), row=1, col=2)
    
    # Quality Performance
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=first_time_right_rate,
        title={'text': "Quality %", 'font': {'size': 14}},
        gauge={
            'axis': {'range': [None, 100], 'tickfont': {'size': 10}},
            'bar': {'color': COLORS['info']},
            'steps': [
                {'range': [0, 80], 'color': '#f1f5f9'},
                {'range': [80, 95], 'color': '#fef3c7'},
                {'range': [95, 100], 'color': '#d1fae5'}
            ],
            'threshold': {
                'line': {'color': COLORS['danger'], 'width': 3},
                'thickness': 0.75,
                'value': 95
            }
        }
    ), row=1, col=3)
    
    fig.update_layout(
        height=350,
        font={'family': 'Inter, sans-serif', 'color': COLORS['dark']},
        paper_bgcolor='white',
        plot_bgcolor='white'
    )
    
    return fig

@app.callback(Output('executive-curves', 'figure'),
              Input('main-tabs', 'value'))
def update_executive_curves(tab):
    """Earned value curves comparison"""
    fig = go.Figure()
    
    # Planned Value
    fig.add_trace(go.Scatter(
        x=time_series['date'],
        y=time_series['planned_value'],
        mode='lines',
        name='Planned Value',
        line=dict(color=COLORS['muted'], width=2, dash='dash'),
        hovertemplate='<b>Planned Value</b><br>Date: %{x}<br>Value: €%{y:,.0f}<extra></extra>'
    ))
    
    # Traditional EV
    fig.add_trace(go.Scatter(
        x=time_series['date'],
        y=time_series['earned_value_traditional'],
        mode='lines',
        name='Traditional EV',
        line=dict(color=COLORS['warning'], width=2),
        hovertemplate='<b>Traditional EV</b><br>Date: %{x}<br>Value: €%{y:,.0f}<extra></extra>'
    ))
    
    # Quality-Gated EV
    fig.add_trace(go.Scatter(
        x=time_series['date'],
        y=time_series['earned_value_quality_gated'],
        mode='lines',
        name='Quality-Gated EV',
        line=dict(color=COLORS['primary'], width=3),
        hovertemplate='<b>Quality-Gated EV</b><br>Date: %{x}<br>Value: €%{y:,.0f}<extra></extra>'
    ))
    
    # Actual Cost
    fig.add_trace(go.Scatter(
        x=time_series['date'],
        y=time_series['actual_cost'],
        mode='lines',
        name='Actual Cost',
        line=dict(color=COLORS['danger'], width=2),
        hovertemplate='<b>Actual Cost</b><br>Date: %{x}<br>Value: €%{y:,.0f}<extra></extra>'
    ))
    
    return apply_modern_layout(fig, "Earned Value Analysis", 350)

# ============================================================================
# DETAILED EVM TAB CALLBACKS
# ============================================================================

@app.callback(Output('detailed-ev-comparison', 'figure'),
              Input('main-tabs', 'value'))
def update_detailed_ev_comparison(tab):
    """EV overstatement visualization"""
    fig = go.Figure()
    
    # Traditional EV
    fig.add_trace(go.Scatter(
        x=time_series['date'],
        y=time_series['earned_value_traditional'],
        mode='lines',
        name='Traditional EV',
        line=dict(color=COLORS['warning'], width=3),
        hovertemplate='<b>Traditional EV</b><br>%{x}<br>€%{y:,.0f}<extra></extra>'
    ))
    
    # Quality-Gated EV
    fig.add_trace(go.Scatter(
        x=time_series['date'],
        y=time_series['earned_value_quality_gated'],
        mode='lines',
        name='Quality-Gated EV',
        line=dict(color=COLORS['primary'], width=3),
        hovertemplate='<b>Quality-Gated EV</b><br>%{x}<br>€%{y:,.0f}<extra></extra>'
    ))
    
    # Fill overstatement area
    fig.add_trace(go.Scatter(
        x=time_series['date'].tolist() + time_series['date'].tolist()[::-1],
        y=time_series['earned_value_traditional'].tolist() + time_series['earned_value_quality_gated'].tolist()[::-1],
        fill='toself',
        fillcolor='rgba(239, 68, 68, 0.1)',
        line=dict(color='rgba(255,255,255,0)'),
        name='EV Overstatement',
        hoverinfo="skip",
        showlegend=True
    ))
    
    return apply_modern_layout(fig, "EV Overstatement Analysis")

@app.callback(Output('detailed-variance-analysis', 'figure'),
              Input('main-tabs', 'value'))
def update_detailed_variance_analysis(tab):
    """Variance analysis over time"""
    time_series['schedule_variance'] = time_series['earned_value_quality_gated'] - time_series['planned_value']
    time_series['cost_variance'] = time_series['earned_value_quality_gated'] - time_series['actual_cost']
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Scatter(
            x=time_series['date'], 
            y=time_series['schedule_variance'],
            mode='lines+markers',
            name='Schedule Variance',
            line=dict(color=COLORS['info'], width=2),
            marker=dict(size=4),
            hovertemplate='<b>Schedule Variance</b><br>%{x}<br>€%{y:,.0f}<extra></extra>'
        ),
        secondary_y=False,
    )
    
    fig.add_trace(
        go.Scatter(
            x=time_series['date'], 
            y=time_series['cost_variance'],
            mode='lines+markers',
            name='Cost Variance',
            line=dict(color=COLORS['danger'], width=2),
            marker=dict(size=4),
            hovertemplate='<b>Cost Variance</b><br>%{x}<br>€%{y:,.0f}<extra></extra>'
        ),
        secondary_y=True,
    )
    
    # Add zero reference lines
    fig.add_hline(y=0, line_dash="dot", line_color=COLORS['muted'], opacity=0.5)
    
    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text="Schedule Variance (€)", secondary_y=False)
    fig.update_yaxes(title_text="Cost Variance (€)", secondary_y=True)
    
    return apply_modern_layout(fig, "Variance Analysis")

@app.callback(Output('detailed-performance-indices', 'figure'),
              Input('main-tabs', 'value'))
def update_detailed_performance_indices(tab):
    """Performance indices comparison"""
    time_series['spi_traditional'] = time_series['earned_value_traditional'] / time_series['planned_value']
    time_series['spi_quality'] = time_series['earned_value_quality_gated'] / time_series['planned_value']
    time_series['cpi'] = time_series['earned_value_quality_gated'] / time_series['actual_cost']
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=time_series['date'],
        y=time_series['spi_traditional'],
        mode='lines+markers',
        name='Traditional SPI',
        line=dict(color=COLORS['warning'], width=2),
        marker=dict(size=4),
        hovertemplate='<b>Traditional SPI</b><br>%{x}<br>%{y:.3f}<extra></extra>'
    ))
    
    fig.add_trace(go.Scatter(
        x=time_series['date'],
        y=time_series['spi_quality'],
        mode='lines+markers',
        name='Quality-Gated SPI',
        line=dict(color=COLORS['primary'], width=3),
        marker=dict(size=5),
        hovertemplate='<b>Quality-Gated SPI</b><br>%{x}<br>%{y:.3f}<extra></extra>'
    ))
    
    fig.add_trace(go.Scatter(
        x=time_series['date'],
        y=time_series['cpi'],
        mode='lines+markers',
        name='Cost Performance Index',
        line=dict(color=COLORS['success'], width=2),
        marker=dict(size=4),
        hovertemplate='<b>CPI</b><br>%{x}<br>%{y:.3f}<extra></extra>'
    ))
    
    # Target line
    fig.add_hline(y=1.0, line_dash="dash", line_color=COLORS['muted'], 
                  annotation_text="Target (1.0)", annotation_position="top right")
    
    return apply_modern_layout(fig, "Performance Indices")

@app.callback(Output('detailed-method-comparison', 'figure'),
              Input('main-tabs', 'value'))
def update_detailed_method_comparison(tab):
    """Method comparison table"""
    comparison_data = {
        'Metric': ['Final SPI', 'Final CPI', 'Schedule Variance', 'Cost Variance', 'Early Warning', 'False Progress'],
        'Traditional EVM': [f'{final_spi_traditional:.3f}', f'{final_cpi_traditional:.3f}', 
                           f'€{schedule_variance:,.0f}', f'€{cost_variance:,.0f}', 'None', 'Hidden'],
        'Quality-Gated EVM': [f'{final_spi_quality:.3f}', f'{final_cpi_quality:.3f}', 
                             f'€{schedule_variance:,.0f}', f'€{cost_variance:,.0f}', '3-5 days', 'Prevented'],
        'Improvement': ['Same', 'More Accurate', 'Same', 'More Accurate', 'Significant', 'Major']
    }
    
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=list(comparison_data.keys()),
            fill_color=COLORS['primary'],
            font=dict(color='white', size=13, family='Inter'),
            align="center",
            height=40
        ),
        cells=dict(
            values=[comparison_data[k] for k in comparison_data.keys()],
            fill_color=[['white', '#f8fafc']*3],
            align="center",
            font=dict(size=12, family='Inter', color=COLORS['dark']),
            height=35
        )
    )])
    
    fig.update_layout(
        title={
            'text': "EVM Method Comparison",
            'x': 0.5,
            'font': {'size': 16, 'color': COLORS['dark'], 'family': 'Inter'}
        },
        height=350,
        margin={'l': 20, 'r': 20, 't': 60, 'b': 20},
        font={'family': 'Inter, sans-serif'}
    )
    
    return fig

# ============================================================================
# QUALITY TAB CALLBACKS
# ============================================================================

@app.callback(Output('quality-status-distribution', 'figure'),
              Input('main-tabs', 'value'))
def update_quality_status_distribution(tab):
    """Quality status pie chart"""
    status_counts = quality_data['status'].value_counts()
    
    colors = [COLORS['success'], COLORS['danger'], COLORS['warning']]
    
    fig = go.Figure(data=[go.Pie(
        labels=status_counts.index,
        values=status_counts.values,
        hole=.4,
        marker_colors=colors,
        textinfo='label+percent',
        textfont={'size': 12, 'family': 'Inter'},
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
    )])
    
    fig.update_layout(
        annotations=[dict(
            text=f'<b>{len(quality_data)}</b><br>Total<br>Inspections', 
            x=0.5, y=0.5, 
            font_size=14, 
            font_family='Inter',
            font_color=COLORS['dark'],
            showarrow=False
        )]
    )
    
    return apply_modern_layout(fig, "Inspection Status Distribution", 350)

@app.callback(Output('quality-step-performance', 'figure'),
              Input('main-tabs', 'value'))
def update_quality_step_performance(tab):
    """Quality performance by step"""
    colors = [COLORS['danger'] if rate > 5 else COLORS['warning'] if rate > 2 else COLORS['success'] 
              for rate in step_performance_df['Failure_Rate']]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=step_performance_df['stepId'],
        y=step_performance_df['Pass_Rate'],
        name='Pass Rate (%)',
        marker_color=COLORS['success'],
        text=[f'{rate:.1f}%' for rate in step_performance_df['Pass_Rate']],
        textposition='auto',
        textfont={'size': 10, 'color': 'white'},
        hovertemplate='<b>%{x}</b><br>Pass Rate: %{y:.1f}%<extra></extra>'
    ))
    
    fig.add_trace(go.Bar(
        x=step_performance_df['stepId'],
        y=step_performance_df['Failure_Rate'],
        name='Failure Rate (%)',
        marker_color=colors,
        text=[f'{rate:.1f}%' for rate in step_performance_df['Failure_Rate']],
        textposition='auto',
        textfont={'size': 10, 'color': 'white'},
        hovertemplate='<b>%{x}</b><br>Failure Rate: %{y:.1f}%<extra></extra>'
    ))
    
    fig.update_layout(barmode='group')
    return apply_modern_layout(fig, "Quality Performance by ITP Step")

@app.callback(Output('quality-cost-impact', 'figure'),
              Input('main-tabs', 'value'))
def update_quality_cost_impact(tab):
    """Rework cost impact"""
    cost_data = task_progress.groupby('stepId')['rework_cost'].sum().reset_index()
    cost_data = cost_data[cost_data['rework_cost'] > 0]
    
    if cost_data.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No rework costs to display",
            xref="paper", yref="paper",
            x=0.5, y=0.5, xanchor='center', yanchor='middle',
            showarrow=False,
            font={'size': 14, 'color': COLORS['muted']}
        )
        return apply_modern_layout(fig, "Rework Cost Impact")
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=cost_data['stepId'],
        y=cost_data['rework_cost'],
        name='Rework Cost',
        marker_color=COLORS['danger'],
        text=[f'€{cost:,.0f}' for cost in cost_data['rework_cost']],
        textposition='auto',
        textfont={'size': 10, 'color': 'white'},
        hovertemplate='<b>%{x}</b><br>Rework Cost: €%{y:,.0f}<extra></extra>'
    ))
    
    return apply_modern_layout(fig, "Rework Cost by ITP Step")

@app.callback(Output('quality-timeline', 'figure'),
              Input('main-tabs', 'value'))
def update_quality_timeline(tab):
    """Quality events timeline"""
    quality_data['date'] = quality_data['inspectedAt'].dt.date
    daily_quality = quality_data.groupby(['date', 'status']).size().reset_index(name='count')
    
    fig = go.Figure()
    
    colors = {'Pass': COLORS['success'], 'Fail': COLORS['danger'], 'Offered': COLORS['warning']}
    for status in ['Pass', 'Fail', 'Offered']:
        status_data = daily_quality[daily_quality['status'] == status]
        if not status_data.empty:
            fig.add_trace(go.Scatter(
                x=status_data['date'],
                y=status_data['count'],
                mode='markers+lines',
                name=f'{status} Events',
                marker=dict(color=colors[status], size=8),
                line=dict(color=colors[status], width=2),
                hovertemplate=f'<b>{status} Events</b><br>%{{x}}<br>Count: %{{y}}<extra></extra>'
            ))
    
    return apply_modern_layout(fig, "Quality Events Timeline")

# ============================================================================
# TEMPORAL TAB CALLBACKS
# ============================================================================

@app.callback(Output('temporal-timeline', 'figure'),
              Input('main-tabs', 'value'))
def update_temporal_timeline(tab):
    """Daily inspection timeline"""
    quality_data['date'] = quality_data['inspectedAt'].dt.date
    daily_stats = quality_data.groupby(['date', 'status']).size().reset_index(name='count')
    
    fig = go.Figure()
    
    colors = {'Pass': COLORS['success'], 'Fail': COLORS['danger'], 'Offered': COLORS['warning']}
    for status in ['Pass', 'Fail', 'Offered']:
        status_data = daily_stats[daily_stats['status'] == status]
        if not status_data.empty:
            fig.add_trace(go.Scatter(
                x=status_data['date'],
                y=status_data['count'],
                mode='markers+lines',
                name=f'{status} Inspections',
                marker=dict(color=colors[status], size=8),
                line=dict(color=colors[status], width=3),
                hovertemplate=f'<b>{status}</b><br>%{{x}}<br>Count: %{{y}}<extra></extra>'
            ))
    
    return apply_modern_layout(fig, "Daily Inspection Events")

@app.callback(Output('temporal-response', 'figure'),
              Input('main-tabs', 'value'))
def update_temporal_response(tab):
    """Response time analysis"""
    if response_df.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No response time data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, xanchor='center', yanchor='middle',
            showarrow=False,
            font={'size': 14, 'color': COLORS['muted']}
        )
        return apply_modern_layout(fig, "Response Time Analysis")
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=response_df['stepId'],
        y=response_df['response_time_hours'],
        name='Response Time (hours)',
        marker_color=COLORS['danger'],
        text=[f'{h:.1f}h' for h in response_df['response_time_hours']],
        textposition='auto',
        textfont={'size': 10, 'color': 'white'},
        hovertemplate='<b>%{x}</b><br>Response Time: %{y:.1f} hours<extra></extra>'
    ))
    
    # Target line
    fig.add_hline(y=6, line_dash="dash", line_color=COLORS['success'], 
                  annotation_text="Target (6h)", annotation_position="top right")
    
    return apply_modern_layout(fig, "Failure Response Time Analysis")

@app.callback(Output('temporal-rework', 'figure'),
              Input('main-tabs', 'value'))
def update_temporal_rework(tab):
    """Rework cycle analysis"""
    if rework_df.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No rework cycle data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, xanchor='center', yanchor='middle',
            showarrow=False,
            font={'size': 14, 'color': COLORS['muted']}
        )
        return apply_modern_layout(fig, "Rework Cycle Analysis")
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=rework_df['stepId'],
        y=rework_df['rework_time_days'],
        name='Rework Cycle (days)',
        marker_color=COLORS['warning'],
        text=[f'{d:.1f}d' for d in rework_df['rework_time_days']],
        textposition='auto',
        textfont={'size': 10, 'color': 'white'},
        hovertemplate='<b>%{x}</b><br>Rework Time: %{y:.1f} days<extra></extra>'
    ))
    
    # Target line
    fig.add_hline(y=0.25, line_dash="dash", line_color=COLORS['success'], 
                  annotation_text="Target (0.25d)", annotation_position="top right")
    
    return apply_modern_layout(fig, "Complete Rework Cycle Analysis")

@app.callback(Output('temporal-delay', 'figure'),
              Input('main-tabs', 'value'))
def update_temporal_delay(tab):
    """Quality delay visualization"""
    if rework_df.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No quality delay data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, xanchor='center', yanchor='middle',
            showarrow=False,
            font={'size': 14, 'color': COLORS['muted']}
        )
        return apply_modern_layout(fig, "Quality Delay Impact")
    
    # Create cumulative delay timeline
    project_dates = pd.date_range(start='2025-07-04', end='2025-07-19', freq='D')
    cumulative_delay = []
    total_delay = 0
    
    for i, date in enumerate(project_dates):
        daily_delay = total_quality_delay / len(project_dates)
        total_delay += daily_delay
        cumulative_delay.append(total_delay / 24)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=project_dates,
        y=cumulative_delay,
        mode='lines',
        fill='tozeroy',
        name='Cumulative Quality Delay',
        line=dict(color=COLORS['danger'], width=3),
        fillcolor=f'rgba(239, 68, 68, 0.1)',
        hovertemplate='<b>Quality Delay</b><br>%{x}<br>%{y:.1f} days<extra></extra>'
    ))
    
    return apply_modern_layout(fig, "Cumulative Quality Delay Impact")

# ============================================================================
# BOTTLENECK TAB CALLBACKS
# ============================================================================

@app.callback(Output('bottleneck-waterfall', 'figure'),
              Input('main-tabs', 'value'))
def update_bottleneck_waterfall(tab):
    """Delay waterfall analysis"""
    categories = ['Baseline', 'Response Delay', 'Rework Delay', 'Total Impact']
    values = [0, avg_response_time/24, avg_rework_time, (avg_response_time/24 + avg_rework_time)]
    
    fig = go.Figure(go.Waterfall(
        name="Quality Delay Sources",
        orientation="v",
        measure=["relative", "relative", "relative", "total"],
        x=categories,
        textposition="outside",
        text=[f"{v:.1f}d" for v in values],
        y=values,
        connector={"line": {"color": COLORS['muted']}},
        increasing={"marker": {"color": COLORS['danger']}},
        decreasing={"marker": {"color": COLORS['success']}},
        totals={"marker": {"color": COLORS['info']}},
        hovertemplate='<b>%{x}</b><br>%{y:.1f} days<extra></extra>'
    ))
    
    return apply_modern_layout(fig, "Quality Delay Waterfall")

@app.callback(Output('bottleneck-steps', 'figure'),
              Input('main-tabs', 'value'))
def update_bottleneck_steps(tab):
    """Step bottleneck analysis"""
    colors = [COLORS['danger'] if rate > 5 else COLORS['warning'] if rate > 2 else COLORS['success'] 
              for rate in step_performance_df['Failure_Rate']]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=step_performance_df['stepId'],
        y=step_performance_df['Failure_Rate'],
        name='Failure Rate (%)',
        marker_color=colors,
        text=[f'{rate:.1f}%' for rate in step_performance_df['Failure_Rate']],
        textposition='auto',
        textfont={'size': 10, 'color': 'white'},
        hovertemplate='<b>%{x}</b><br>Failure Rate: %{y:.1f}%<extra></extra>'
    ))
    
    # Target line
    fig.add_hline(y=2, line_dash="dash", line_color=COLORS['success'], 
                  annotation_text="Target (2%)", annotation_position="top right")
    
    return apply_modern_layout(fig, "Failure Rate by ITP Step")

# ============================================================================
# TASK TAB CALLBACKS
# ============================================================================

@app.callback(Output('task-gantt', 'figure'),
              Input('main-tabs', 'value'))
def update_task_gantt(tab):
    """Task duration visualization"""
    sample_tasks = task_progress.head(10).copy()
    sample_tasks['duration'] = (sample_tasks['pass_date'] - sample_tasks['offered_date']).dt.days
    
    colors = [COLORS['danger'] if failures > 0 else COLORS['success'] for failures in sample_tasks['failure_count']]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=sample_tasks['duration'],
        y=sample_tasks['stepId'],
        orientation='h',
        name='Task Duration',
        marker_color=colors,
        text=[f'{d}d' for d in sample_tasks['duration']],
        textposition='auto',
        textfont={'size': 10, 'color': 'white'},
        hovertemplate='<b>%{y}</b><br>Duration: %{x} days<extra></extra>'
    ))
    
    return apply_modern_layout(fig, "Task Duration Analysis (Sample)")

@app.callback(Output('task-performance', 'figure'),
              Input('main-tabs', 'value'))
def update_task_performance(tab):
    """Task performance summary"""
    step_summary = task_progress.groupby('stepId').agg({
        'planned_value': 'sum',
        'earned_value_quality_gated': 'sum',
        'actual_cost': 'sum',
        'failure_count': 'sum'
    }).reset_index()
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Bar(
            x=step_summary['stepId'], 
            y=step_summary['planned_value'],
            name='Planned Value', 
            marker_color=COLORS['info'],
            hovertemplate='<b>%{x}</b><br>Planned: €%{y:,.0f}<extra></extra>'
        ),
        secondary_y=False,
    )
    
    fig.add_trace(
        go.Bar(
            x=step_summary['stepId'], 
            y=step_summary['earned_value_quality_gated'],
            name='Earned Value', 
            marker_color=COLORS['success'],
            hovertemplate='<b>%{x}</b><br>Earned: €%{y:,.0f}<extra></extra>'
        ),
        secondary_y=False,
    )
    
    fig.add_trace(
        go.Scatter(
            x=step_summary['stepId'], 
            y=step_summary['failure_count'],
            mode='markers+lines', 
            name='Failures',
            marker=dict(size=10, color=COLORS['danger']),
            line=dict(color=COLORS['danger'], width=2),
            hovertemplate='<b>%{x}</b><br>Failures: %{y}<extra></extra>'
        ),
        secondary_y=True,
    )
    
    fig.update_xaxes(title_text="ITP Step")
    fig.update_yaxes(title_text="Value (€)", secondary_y=False)
    fig.update_yaxes(title_text="Failure Count", secondary_y=True)
    
    return apply_modern_layout(fig, "Performance Summary by Step")

# ============================================================================
# SIMULATION TAB CALLBACKS
# ============================================================================

@app.callback(Output('simulation-comparison', 'figure'),
              Input('main-tabs', 'value'))
def update_simulation_comparison(tab):
    """Improvement scenario comparison"""
    scenarios = ['Current', 'Perfect Quality', 'Fast Response', 'Combined']
    costs = [final_ac, total_budget, total_budget + (total_rework_cost * 0.25 / 4.1), total_budget + (total_rework_cost * 0.4)]
    savings = [0, total_rework_cost, total_rework_cost * (1 - 0.25/4.1), total_rework_cost * 0.6]
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    colors = [COLORS['danger'], COLORS['success'], COLORS['info'], COLORS['primary']]
    
    fig.add_trace(
        go.Bar(
            x=scenarios, 
            y=costs, 
            name='Total Cost (€)', 
            marker_color=colors,
            text=[f'€{cost:,.0f}' for cost in costs],
            textposition='auto',
            textfont={'size': 10, 'color': 'white'},
            hovertemplate='<b>%{x}</b><br>Total Cost: €%{y:,.0f}<extra></extra>'
        ),
        secondary_y=False,
    )
    
    fig.add_trace(
        go.Scatter(
            x=scenarios, 
            y=savings, 
            mode='markers+lines',
            name='Savings (€)', 
            marker=dict(size=12, color=COLORS['warning']),
            line=dict(color=COLORS['warning'], width=3),
            text=[f'€{saving:,.0f}' for saving in savings],
            textposition='top center',
            textfont={'size': 10, 'color': COLORS['warning']},
            hovertemplate='<b>%{x}</b><br>Savings: €%{y:,.0f}<extra></extra>'
        ),
        secondary_y=True,
    )
    
    fig.update_xaxes(title_text="Improvement Scenario")
    fig.update_yaxes(title_text="Total Cost (€)", secondary_y=False)
    fig.update_yaxes(title_text="Savings (€)", secondary_y=True)
    
    return apply_modern_layout(fig, "Project Cost Simulation", 450)

