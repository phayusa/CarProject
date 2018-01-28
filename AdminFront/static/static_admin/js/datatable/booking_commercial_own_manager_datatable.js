/*
Name: 			Tables / Ajax - Examples
Written by: 	Okler Themes - (http://www.okler.net)
Theme Version: 	2.0.0
*/

(function ($) {

    'use strict';

    var datatableInit = function () {

        var $table = $('#booking_commercial_table');
        // $table.dataTable({
        // 	dom: '<"row"<"col-lg-6"l><"col-lg-6"f>><"table-responsive"t>p',
        // 	bProcessing: true,
        // 	sAjaxSource: $table.data('url')
        // });
        var bis = $table.DataTable({
                // "ajax": $table.data('url'),
                "ajax": {
                    url: $table.data('url'),
                    dataSrc: ''
                },
                dom: '<"row"<"col-lg-6"l><"col-lg-6"f>><"table-responsive"t>p',
                bProcessing: true,
                columns: [
                    {
                        "data": "date",
                        "type": "date",
                        "render": function (value) {
                            if (value === null) return "";
                            var dt = new Date(value);
                            return (dt.getDate() + 1) + "/" + (dt.getMonth() + 1) + "/" + dt.getFullYear();
                        }
                    },
                    {data: 'airport'},
                    {data: 'destination'},
                    // {data: 'date'},
                    {data: 'client'},
                    // {data: 'arrive_time'},
                    {
                        "data": "arrive_time",
                        "type": "date",
                        "render": function (value) {
                            if (value === null) return "";

                            var dt = new Date(value);
                            return (dt.getDate() + 1) + "/" + (dt.getMonth() +1) + "/" + dt.getFullYear() + " " + dt.getUTCHours() + "H" + dt.getUTCMinutes();
                        }
                    },
                    {data: 'status'},
                    {data: 'tt'}
                ],
                "columnDefs": [{
                    "targets": -1,
                    "data": null,
                    "defaultContent": "<button class=\"btn btn-primary\" >Editer</button>"
                    // "defaultContent": "<button class=\"btn btn-primary\" data-toggle=\"modal\" data-target=\"#modalForm\"\n" +
                    // "                                                    onclick=\"changeSelect({{ car.id }})\">Réserver\n" +
                    // "                                            </button>"
                }],
                // "fnCreatedRow": function (nRow, aData, iDataIndex) {
                //     $('td:eq(6)', nRow).append("<div class='col1d'><button class='editBut'>Ta mere</button></div>");
                // },
                "language": {
                    "sProcessing": "Traitement en cours...",
                    "sSearch": "Rechercher&nbsp;:",
                    "sLengthMenu": "Afficher _MENU_ &eacute;l&eacute;ments",
                    "sInfo": "Affichage de l'&eacute;l&eacute;ment _START_ &agrave; _END_ sur _TOTAL_ &eacute;l&eacute;ments",
                    "sInfoEmpty": "Affichage de l'&eacute;l&eacute;ment 0 &agrave; 0 sur 0 &eacute;l&eacute;ment",
                    "sInfoFiltered": "(filtr&eacute; de _MAX_ &eacute;l&eacute;ments au total)",
                    "sInfoPostFix": "",
                    "sLoadingRecords": "Chargement en cours...",
                    "sZeroRecords": "Aucun &eacute;l&eacute;ment &agrave; afficher",
                    "sEmptyTable": "Aucune donn&eacute;e disponible dans le tableau",
                    "oPaginate": {
                        "sFirst": "Premier",
                        "sPrevious": "Pr&eacute;c&eacute;dent",
                        "sNext": "Suivant",
                        "sLast": "Dernier"
                    },
                    "oAria": {
                        "sSortAscending": ": activer pour trier la colonne par ordre croissant",
                        "sSortDescending": ": activer pour trier la colonne par ordre d&eacute;croissant"
                    }
                }
            }
        );

        $('#booking_commercial_table tbody').on('click', 'button', function () {
            // var data = bis.row($(this).parents('tr')).data();
            // alert("" + data["id"]);
            // $('#id01').modal('show');
            window.location.href = '/commercial/' + bis.row($(this).parents('tr')).data()["id"];
            // $('#modalForm').getElementById("")
        });

        // Add the class for the search field is inside the table
        $("#booking_commercial_table_filter").addClass("col-md-10");

    };


    $(function () {
        datatableInit();
        // document.getElementById("edit").
    });

}).apply(this, [jQuery]);