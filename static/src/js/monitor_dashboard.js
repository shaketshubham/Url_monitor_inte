/** @odoo-module **/

import { Component, useState, onWillStart } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";

export class MonitorDashboard extends Component {
    setup() {
        this.rpc = useService("rpc");

        // State to hold the dashboard data
        this.state = useState({
            total_monitors: 0,
            down_monitors: 0,
            uptime_24h: 0,
        });

        onWillStart(() => this.fetchDashboardData());
    }

    // Method to fetch dashboard data from Odoo model method
    async fetchDashboardData() {
        try {
            const data = await this.rpc("/url_monitor_integration/dashboard_data", {});
            this.state.total_monitors = data.total_monitors;
            this.state.down_monitors = data.down_monitors;
            this.state.uptime_24h = data.uptime_24h;
        } catch (error) {
            console.error("Error fetching dashboard data:", error);
        }
    }
}

// Register component and its template
MonitorDashboard.template = "url_monitor_integration.MonitorDashboard";
registry.category("actions").add("url_monitor_integration.action_monitor_dashboard", MonitorDashboard);
