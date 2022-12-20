let privacyContent = document.getElementById("privacyContent")
privacy()

function privacy() {
    privacyContent.innerHTML = `<div class="modal-header">
    <h5 class="modal-title" id="staticBackdropLabel" style="text-align:center;text-decoration: underline; font-weight: bold;font-size: large;">
        Terms and Conditions
    </h5>
    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
</div>
<div class="modal-body">
    <h4 class="privacyHead">Privacy Policy</h4>
    <p class="privacyDetails"> ALLORA is built as a Free Ecommerce web. This SERVICE is provided by Allora.dev at no cost (However in-site purchases are excluded) and is intended for use as is. This page is used to inform visitors regarding our policies with the collection, use, and disclosure of Personal
        Information if anyone decided to use our Service. If you choose to use our Service, then you agree to the collection and use of information in relation to this policy. The Personal Information that We collect is used for providing
        and improving the Service. we will not use or share your information with anyone except as described in this Privacy Policy. The terms used in this Privacy Policy have the same meanings as in our Terms and Conditions, which is accessible
        at Allora.dev unless otherwise defined in this Privacy Policy.</p>
    <hr>
    <h4 class="privacyHead">Information Collection and Use</h4>
    <p class="privacyDetails">
        For a better experience, while using our Service, we may require you to provide us with certain personally identifiable information, including but not limited to nothing. The information that We request will be retained on your device and is not collected
        by us in any way. The Website does use third party services that may collect information used to identify you.

        <br> We want to inform you that whenever you use our Service, in a case of an error in the Website We collect data and information (through third party products) on your phone called Log Data. This Log Data may include information
        such as your device Internet Protocol (“IP”) address, device name, operating system version, the configuration of the Website when utilizing our Service, the time and date of your use of the Service, and other statistics.
    </p>
    <hr>
    <h4 class="privacyHead"> Cookies</h4>
    <p class="privacyDetails">
        Cookies are files with a small amount of data that are commonly used as anonymous unique identifiers. These are sent to your browser from the websites that you visit and are stored on your device's internal memory. This Service does not use these “cookies”
        explicitly. However, the Web may use third party code and libraries that use “cookies” to collect information and improve their services. You have the option to either accept or refuse these cookies and know when a cookie is being
        sent to your device. If you choose to refuse our cookies, you may not be able to use some portions of this Service.
    </p>
    <hr>
    <h4 class="privacyHead">Service Providers</h4>
    <p class="privacyDetails">
        We may employ third-party companies and individuals due to the following reasons: To facilitate our Service; To provide the Service on our behalf; To perform Service-related services; or To assist us in analyzing how our Service is used. We want to inform
        users of this Service that these third parties have access to your Personal Information. The reason is to perform the tasks assigned to them on our behalf. However, they are obligated not to disclose or use the information for
        any other purpose.
    </p>
    <hr>
    <h4 class="privacyHead"> Security</h4>
    <p class="privacyDetails">
        We value your trust in providing us your Personal Information, thus we are striving to use commercially acceptable means of protecting it. But remember that no method of transmission over the internet, or method of electronic storage is 100% secure and
        reliable, and We cannot guarantee its absolute security.
    </p>
    <hr>
    <h4 class="privacyHead">Links to Other Sites</h4>
    <p class="privacyDetails">
        This Service may contain links to other sites. If you click on a third-party link, you will be directed to that site. Note that these external sites are not operated by us. Therefore, We strongly advise you to review the Privacy Policy of these websites.
        We have no control over and assume no responsibility for the content, privacy policies, or practices of any third-party sites or services.
    </p>
    <hr>
    <h4 class="privacyHead">Children’s Privacy</h4>
    <p class="privacyDetails">
        These Services do not address anyone under the age of 12. We do not knowingly collect personally identifiable information from children under 12 years of age. In the case We discover that a child under 12 has provided us with personal information, We immediately
        delete this from our servers. If you are a parent or guardian and you are aware that your child has provided us with personal information, please contact us so that We will be able to do necessary actions.</p>
    <hr>
    <h4 class="privacyHead">
        Changes to This Privacy Policy</h4>
    <p class="privacyDetails">
    We may update our Privacy Policy from time to time. Thus, you are advised to review this page periodically for any changes. We will notify you of any changes by posting the new Privacy Policy on this page. This policy is effective as of 10-11-2022</p>
    <hr>
    <h4 class="privacyHead">
        Contact Us</h4>
    <p class="privacyDetails">
        If you have any questions or suggestions about our Privacy Policy, do not hesitate to contact us
        <a href="/contact">Here</a>
    </p>
    <hr>
</div>
<div class="modal-footer">
    <!-- <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button> -->
    <button type="button" data-bs-dismiss="modal" class="btn btn-primary">Understood</button>
</div>`;
}