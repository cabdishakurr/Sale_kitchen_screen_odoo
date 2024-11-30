/** @odoo-module */

import { registry } from "@web/core/registry";
const { Component, onWillStart, useState, onMounted } = owl;
import { useService } from "@web/core/utils/hooks";


class kitchen_screen_dashboard extends Component {

    setup() {
        super.setup();
        this.busService = this.env.services.bus_service;
        this.busService.addChannel("sale_order_created");
        onWillStart(() => {
            this.busService.addEventListener('notification', this.onSaleOrderCreation.bind(this));
        })
        this.action = useService("action");
        this.rpc = this.env.services.rpc;
        this.orm = useService("orm");
        
        this.state = useState({
            order_details: [],
            website_id: null,
            stages: 'draft',
            draft_count: [],
            waiting_count: [],
            ready_count: [],
            lines: []
        });

        // Get website_id from context or session storage
        const website_id = this.props.action.context.default_website_id 
            || sessionStorage.getItem('website_id');
        
        if (website_id) {
            this.website_id = parseInt(website_id, 10);
            sessionStorage.setItem('website_id', website_id);
            this.loadOrders();
        }
    }

    async loadOrders() {
        const result = await this.orm.call(
            "sale.order",
            "get_kitchen_orders",
            [this.website_id]
        );
        
        this.state.order_details = result.orders;
        this.state.lines = result.order_lines;
        this.updateCounts();
    }

    updateCounts() {
        this.state.draft_count = this.state.order_details.filter(
            order => order.order_status == 'draft' 
            && order.website_id[0] == this.website_id
        ).length;
        
        this.state.waiting_count = this.state.order_details.filter(
            order => order.order_status == 'waiting' 
            && order.website_id[0] == this.website_id
        ).length;
        
        this.state.ready_count = this.state.order_details.filter(
            order => order.order_status == 'ready' 
            && order.website_id[0] == this.website_id
        ).length;
    }

    //Calling the onPosOrderCreation when an order is created or edited on the backend and return the notification
    onPosOrderCreation(message){
        let payload = message.detail[0].payload
        var self=this
        if(payload.message == "pos_order_created" && payload.res_model == "pos.order"){
            self.orm.call("pos.order", "get_details", ["", self.shop_id,""]).then(function(result) {
            self.state.order_details = result['orders']
            self.state.lines = result['order_lines']
            self.state.shop_id=self.shop_id
            self.state.draft_count=self.state.order_details.filter((order) => order.order_status=='draft' && order.config_id[0]==self.state.shop_id).length
            self.state.waiting_count=self.state.order_details.filter((order) => order.order_status=='waiting' && order.config_id[0]==self.state.shop_id).length
            self.state.ready_count=self.state.order_details.filter((order) => order.order_status=='ready' && order.config_id[0]==self.state.shop_id).length
            });
        }
    }

    // cancel the order from the kitchen
    cancel_order(e) {
         var input_id = $("#" + e.target.id).val();
         this.orm.call("pos.order", "order_progress_cancel", [Number(input_id)])
         var current_order = this.state.order_details.filter((order) => order.id==input_id)
         if(current_order){
            current_order[0].order_status = 'cancel'
         }
    }
    // accept the order from the kitchen
        accept_order(e) {
        var input_id = $("#" + e.target.id).val();
        ScrollReveal().reveal("#" + e.target.id, {
            delay: 1000,
            duration: 2000,
            opacity: 0,
            distance: "50%",
            origin: "top",
            reset: true,
            interval: 600,
        });
         var self=this
         this.orm.call("pos.order", "order_progress_draft", [Number(input_id)])
         var current_order = this.state.order_details.filter((order) => order.id==input_id)
         if(current_order){
            current_order[0].order_status = 'waiting'
         }
    }
    // set the stage is ready to see the completed stage orders
    ready_stage(e) {
        var self = this;
        self.state.stages = 'ready';
    }
    //set the stage is waiting to see the ready stage orders
    waiting_stage(e) {
        var self = this;
        self.state.stages = 'waiting';
    }
    //set the stage is draft to see the cooking stage orders
    draft_stage(e) {
        var self = this;
        self.state.stages = 'draft';
    }
    // change the status of the order from the kitchen
    done_order(e) {
        var self = this;
        var input_id = $("#" + e.target.id).val();
        this.orm.call("pos.order", "order_progress_change", [Number(input_id)])
        var current_order = this.state.order_details.filter((order) => order.id==input_id)
         if(current_order){
            current_order[0].order_status = 'ready'
         }
    }
    // change the status of the product from the kitchen
    accept_order_line(e) {
        var input_id = $("#" + e.target.id).val();
        this.orm.call("pos.order.line", "order_progress_change", [Number(input_id)])
        var current_order_line=this.state.lines.filter((order_line) => order_line.id==input_id)
        if (current_order_line){
            if (current_order_line[0].order_status == 'ready'){
                current_order_line[0].order_status = 'waiting'
            }
            else{
                current_order_line[0].order_status = 'ready'
            }
        }
    }

}
kitchen_screen_dashboard.template = 'KitchenCustomDashBoard';
registry.category("actions").add("kitchen_custom_dashboard_tags", kitchen_screen_dashboard);